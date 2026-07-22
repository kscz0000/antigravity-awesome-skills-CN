# 原生 Android — Java 参考

## 何时使用 Java

Java 仍受到 Android 与 Google 的完整支持。以下场景请使用 Java：
- 维护或扩展现有的 Java 代码库
- 团队熟悉 Java 但无 Kotlin 经验
- 集成仅支持 Java 的 SDK 或遗留模块
- 渐进式迁移：新增 Kotlin 模块，旧模块保留 Java

> **Java + Kotlin 互操作无缝**——同一项目可同时包含两者。新文件可以采用 Kotlin，旧文件保留 Java。

---

## 项目结构

```
app/src/main/java/com/example/app/
├── MyApp.java                   # Application 类
├── MainActivity.java            # 宿主 Activity
├── ui/
│   └── home/
│       ├── HomeActivity.java    # 或基于 Fragment
│       ├── HomeFragment.java
│       └── HomeAdapter.java
├── viewmodel/
│   └── HomeViewModel.java
├── repository/
│   └── ItemRepository.java
├── data/
│   ├── remote/
│   │   ├── ApiService.java      # Retrofit 接口
│   │   ├── ApiClient.java       # OkHttp + Retrofit 配置
│   │   └── dto/ItemDto.java
│   └── local/
│       ├── AppDatabase.java     # Room 数据库
│       ├── ItemDao.java
│       └── entity/ItemEntity.java
├── model/
│   └── Item.java                # 领域模型
└── di/                          # 手动 DI 或 Hilt
```

---

## ViewModel（Java + LiveData）

```java
public class HomeViewModel extends ViewModel {

    private final MutableLiveData<UiState<List<Item>>> _uiState =
        new MutableLiveData<>(UiState.loading());

    public LiveData<UiState<List<Item>>> uiState = _uiState;

    private final ItemRepository repository;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    // 构造函数注入（Hilt 或手动）
    public HomeViewModel(ItemRepository repository) {
        this.repository = repository;
        loadItems();
    }

    public void loadItems() {
        _uiState.setValue(UiState.loading());
        executor.execute(() -> {
            try {
                List<Item> items = repository.getItems();
                _uiState.postValue(UiState.success(items));
            } catch (Exception e) {
                _uiState.postValue(UiState.error(e.getMessage()));
            }
        });
    }

    @Override
    protected void onCleared() {
        super.onCleared();
        executor.shutdown();
    }
}
```

---

## UiState 包装类

```java
public class UiState<T> {
    public enum Status { LOADING, SUCCESS, ERROR }

    public final Status status;
    public final T data;
    public final String errorMessage;

    private UiState(Status status, T data, String errorMessage) {
        this.status = status;
        this.data = data;
        this.errorMessage = errorMessage;
    }

    public static <T> UiState<T> loading() {
        return new UiState<>(Status.LOADING, null, null);
    }

    public static <T> UiState<T> success(T data) {
        return new UiState<>(Status.SUCCESS, data, null);
    }

    public static <T> UiState<T> error(String message) {
        return new UiState<>(Status.ERROR, null, message);
    }

    public boolean isLoading() { return status == Status.LOADING; }
    public boolean isSuccess() { return status == Status.SUCCESS; }
    public boolean isError()   { return status == Status.ERROR; }
}
```

---

## Fragment 监听 ViewModel

```java
public class HomeFragment extends Fragment {

    private HomeViewModel viewModel;
    private FragmentHomeBinding binding; // ViewBinding

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        binding = FragmentHomeBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        viewModel = new ViewModelProvider(this,
            new HomeViewModelFactory(new ItemRepository(requireContext())))
            .get(HomeViewModel.class);

        viewModel.uiState.observe(getViewLifecycleOwner(), state -> {
            binding.progressBar.setVisibility(state.isLoading() ? View.VISIBLE : View.GONE);
            binding.recyclerView.setVisibility(state.isSuccess() ? View.VISIBLE : View.GONE);
            binding.errorView.setVisibility(state.isError() ? View.VISIBLE : View.GONE);

            if (state.isSuccess()) {
                adapter.submitList(state.data);
            }
            if (state.isError()) {
                binding.errorText.setText(state.errorMessage);
            }
        });

        binding.retryButton.setOnClickListener(v -> viewModel.loadItems());
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null; // 关键——避免内存泄漏
    }
}
```

---

## Room 数据库（Java）

```java
// Entity
@Entity(tableName = "items")
public class ItemEntity {
    @PrimaryKey
    @NonNull
    public String id;
    public String title;
    public long updatedAt;

    public ItemEntity(@NonNull String id, String title, long updatedAt) {
        this.id = id;
        this.title = title;
        this.updatedAt = updatedAt;
    }
}

// DAO
@Dao
public interface ItemDao {
    @Query("SELECT * FROM items ORDER BY updatedAt DESC")
    LiveData<List<ItemEntity>> observeAll();

    @Query("SELECT * FROM items ORDER BY updatedAt DESC")
    List<ItemEntity> getAll(); // 阻塞——请在主线程之外调用

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<ItemEntity> items);

    @Query("DELETE FROM items")
    void deleteAll();
}

// Database
@Database(entities = {ItemEntity.class}, version = 1, exportSchema = true)
public abstract class AppDatabase extends RoomDatabase {
    private static volatile AppDatabase INSTANCE;

    public abstract ItemDao itemDao();

    public static AppDatabase getInstance(Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                        context.getApplicationContext(),
                        AppDatabase.class,
                        "app_database"
                    ).build();
                }
            }
        }
        return INSTANCE;
    }
}
```

---

## Retrofit API 客户端（Java）

```java
// 接口
public interface ApiService {
    @GET("items")
    Call<List<ItemDto>> getItems();

    @GET("items/{id}")
    Call<ItemDto> getItemById(@Path("id") String id);

    @POST("items")
    Call<ItemDto> createItem(@Body ItemDto item);
}

// 客户端配置
public class ApiClient {
    private static final String BASE_URL = BuildConfig.API_BASE_URL;
    private static ApiService INSTANCE;

    public static ApiService getInstance() {
        if (INSTANCE == null) {
            OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
                .addInterceptor(new AuthInterceptor())
                .addInterceptor(new HttpLoggingInterceptor()
                    .setLevel(BuildConfig.DEBUG
                        ? HttpLoggingInterceptor.Level.BODY
                        : HttpLoggingInterceptor.Level.NONE))
                .build();

            Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

            INSTANCE = retrofit.create(ApiService.class);
        }
        return INSTANCE;
    }
}

// 鉴权拦截器
public class AuthInterceptor implements Interceptor {
    @NonNull
    @Override
    public Response intercept(@NonNull Chain chain) throws IOException {
        String token = TokenStorage.getInstance().getToken();
        Request request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer " + token)
            .build();
        return chain.proceed(request);
    }
}
```

---

## 仓库（Java）

```java
public class ItemRepository {
    private final ItemDao itemDao;
    private final ApiService apiService;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public ItemRepository(Context context) {
        AppDatabase db = AppDatabase.getInstance(context);
        this.itemDao = db.itemDao();
        this.apiService = ApiClient.getInstance();
    }

    // 同步获取，供 ViewModel 的 executor 使用
    public List<Item> getItems() throws Exception {
        Response<List<ItemDto>> response = apiService.getItems().execute();
        if (response.isSuccessful() && response.body() != null) {
            return response.body().stream()
                .map(ItemMapper::toDomain)
                .collect(Collectors.toList());
        } else {
            throw new IOException("HTTP " + response.code());
        }
    }

    // 监听缓存数据（返回 LiveData，自动更新 UI）
    public LiveData<List<Item>> observeItems() {
        return Transformations.map(itemDao.observeAll(), entities ->
            entities.stream().map(ItemMapper::toDomain).collect(Collectors.toList())
        );
    }

    // 从网络刷新（在后台线程或 executor 中调用）
    public void refreshItems(Callback<Void> callback) {
        executor.execute(() -> {
            try {
                Response<List<ItemDto>> response = apiService.getItems().execute();
                if (response.isSuccessful() && response.body() != null) {
                    List<ItemEntity> entities = response.body().stream()
                        .map(ItemMapper::toEntity)
                        .collect(Collectors.toList());
                    itemDao.deleteAll();
                    itemDao.insertAll(entities);
                    callback.onSuccess(null);
                } else {
                    callback.onError(new IOException("HTTP " + response.code()));
                }
            } catch (IOException e) {
                callback.onError(e);
            }
        });
    }

    public interface Callback<T> {
        void onSuccess(T result);
        void onError(Exception e);
    }
}
```

---

## RecyclerView Adapter（Java）

```java
public class ItemAdapter extends ListAdapter<Item, ItemAdapter.ItemViewHolder> {

    private final OnItemClickListener listener;

    public interface OnItemClickListener {
        void onItemClick(Item item);
    }

    public ItemAdapter(OnItemClickListener listener) {
        super(new DiffUtil.ItemCallback<Item>() {
            @Override
            public boolean areItemsTheSame(@NonNull Item a, @NonNull Item b) {
                return a.getId().equals(b.getId());
            }

            @Override
            public boolean areContentsTheSame(@NonNull Item a, @NonNull Item b) {
                return a.equals(b);
            }
        });
        this.listener = listener;
    }

    @NonNull
    @Override
    public ItemViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        ItemRowBinding binding = ItemRowBinding.inflate(
            LayoutInflater.from(parent.getContext()), parent, false);
        return new ItemViewHolder(binding);
    }

    @Override
    public void onBindViewHolder(@NonNull ItemViewHolder holder, int position) {
        holder.bind(getItem(position), listener);
    }

    static class ItemViewHolder extends RecyclerView.ViewHolder {
        private final ItemRowBinding binding;

        ItemViewHolder(ItemRowBinding binding) {
            super(binding.getRoot());
            this.binding = binding;
        }

        void bind(Item item, OnItemClickListener listener) {
            binding.titleText.setText(item.getTitle());
            binding.getRoot().setOnClickListener(v -> listener.onItemClick(item));
        }
    }
}
```

---

## XML 布局最佳实践（Java 项目）

```xml
<!-- 使用 ConstraintLayout —— 扁平层级 = 更佳性能 -->
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <!-- 始终使用 MaterialTheme 中的 ?attr/ 令牌，禁止硬编码颜色 -->
    <TextView
        android:id="@+id/titleText"
        android:textColor="?attr/colorOnSurface"
        android:textAppearance="?attr/textAppearanceTitleMedium"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

- 始终使用 **ViewBinding**（不使用 `findViewById`，简单场景不使用 DataBinding）
- 在 `build.gradle.kts` 中启用：`viewBinding { enable = true }`
- 在 `onDestroyView()` 中将 `binding` 置空，防止 Fragment 内存泄漏

---

## 错误处理（Java）

```java
// 受检异常：始终显式处理
public Result<List<Item>> getItemsSafe() {
    try {
        Response<List<ItemDto>> response = apiService.getItems().execute();
        if (!response.isSuccessful()) {
            return Result.failure(new HttpException(response));
        }
        List<Item> items = Objects.requireNonNull(response.body())
            .stream().map(ItemMapper::toDomain).collect(Collectors.toList());
        return Result.success(items);
    } catch (IOException e) {
        return Result.failure(new NetworkException("Network error", e));
    } catch (NullPointerException e) {
        return Result.failure(new ParseException("Empty response body", e));
    }
}

// 自定义异常体系
public class AppException extends Exception {
    public AppException(String message) { super(message); }
    public AppException(String message, Throwable cause) { super(message, cause); }
}
public class NetworkException extends AppException { ... }
public class ParseException extends AppException { ... }
public class AuthException extends AppException { ... }
```

---

## Hilt DI（Java）

```java
// Application
@HiltAndroidApp
public class MyApp extends Application {}

// Activity / Fragment —— 标注以便注入
@AndroidEntryPoint
public class HomeFragment extends Fragment {
    @Inject
    ItemRepository repository; // 由 Hilt 注入
}

// ViewModel
@HiltViewModel
public class HomeViewModel extends ViewModel {
    private final ItemRepository repository;

    @Inject
    public HomeViewModel(ItemRepository repository) {
        this.repository = repository;
    }
}

// Module
@Module
@InstallIn(SingletonComponent.class)
public class DatabaseModule {
    @Provides
    @Singleton
    public AppDatabase provideDatabase(@ApplicationContext Context context) {
        return AppDatabase.getInstance(context);
    }

    @Provides
    public ItemDao provideItemDao(AppDatabase db) {
        return db.itemDao();
    }
}
```

---

## 单元测试（Java）

```java
@ExtendWith(MockitoExtension.class)
class HomeViewModelTest {

    @Mock
    ItemRepository mockRepository;

    HomeViewModel viewModel;

    @BeforeEach
    void setup() {
        viewModel = new HomeViewModel(mockRepository);
    }

    @Test
    void loadItems_success_emitsSuccessState() throws Exception {
        List<Item> items = Arrays.asList(new Item("1", "Test"));
        when(mockRepository.getItems()).thenReturn(items);

        viewModel.loadItems();

        // 等待 executor —— 使用 CountDownLatch 或 InstantExecutorRule
        UiState<List<Item>> state = viewModel.uiState.getValue();
        assertNotNull(state);
        assertTrue(state.isSuccess());
        assertEquals(items, state.data);
    }

    @Test
    void loadItems_failure_emitsErrorState() throws Exception {
        when(mockRepository.getItems()).thenThrow(new IOException("Network error"));

        viewModel.loadItems();

        UiState<List<Item>> state = viewModel.uiState.getValue();
        assertNotNull(state);
        assertTrue(state.isError());
    }
}
```

---

## Java → Kotlin 迁移路径

将 Java 项目渐进式迁移至 Kotlin 时：

1. **新文件使用 Kotlin**——Java 与 Kotlin 无缝共存
2. **先迁移工具类**——使用 `@JvmStatic`、`@JvmField` 改善互操作
3. **迁移数据模型**——Java POJO → Kotlin `data class`
4. **迁移 DAO 与仓库**——加入 `suspend` + `Flow`
5. **最后迁移 ViewModel**——将 `LiveData` + `MutableLiveData` 替换为 `StateFlow`
6. **迁移 Activity/Fragment**——逐屏迁移到 Compose
7. 在存在 Java 调用方时，为 Kotlin 添加 `@JvmOverloads`、`@JvmName`

```kotlin
// Kotlin data class 替代 Java POJO
data class Item(
    val id: String,
    val title: String,
    val updatedAt: Long = System.currentTimeMillis()
)

// Kotlin 扩展，干净地从 Kotlin 消费 Java LiveData
fun <T> LiveData<T>.observeNonNull(owner: LifecycleOwner, observer: (T) -> Unit) {
    observe(owner) { it?.let(observer) }
}
```