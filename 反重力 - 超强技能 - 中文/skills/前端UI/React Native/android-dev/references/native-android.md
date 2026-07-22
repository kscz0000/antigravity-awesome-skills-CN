# 原生 Android 参考（Kotlin + Jetpack Compose）

## 项目结构

```
app/
├── src/
│   ├── main/
│   │   ├── AndroidManifest.xml
│   │   ├── java/com.example.app/
│   │   │   ├── MyApp.kt                     # Application 类，Hilt 入口
│   │   │   ├── MainActivity.kt              # 单 Activity，NavHost 宿主
│   │   │   ├── ui/
│   │   │   │   ├── theme/                   # MaterialTheme、Color、Type、Shape
│   │   │   │   ├── components/              # 共享设计系统 Composable
│   │   │   │   └── feature/
│   │   │   │       ├── home/
│   │   │   │       │   ├── HomeScreen.kt
│   │   │   │       │   ├── HomeViewModel.kt
│   │   │   │       │   └── HomeUiState.kt
│   │   │   ├── domain/
│   │   │   │   ├── model/                   # 领域模型（纯 Kotlin，无 Android 依赖）
│   │   │   │   ├── repository/              # 仅接口
│   │   │   │   └── usecase/                 # 每个用例一个类
│   │   │   ├── data/
│   │   │   │   ├── remote/                  # Retrofit 服务、DTO、映射器
│   │   │   │   ├── local/                   # Room 数据库、DAO、Entity
│   │   │   │   └── repository/              # 仓库实现
│   │   │   └── di/                          # Hilt 模块
│   └── test/                                # 单元测试
│   └── androidTest/                         # 仪器化测试
├── build.gradle.kts
└── proguard-rules.pro
```

## ViewModel 模式

```kotlin
// UiState —— sealed class，配合 when() 穷尽匹配
sealed class HomeUiState {
    object Loading : HomeUiState()
    data class Success(val items: List<Item>) : HomeUiState()
    data class Error(val message: String) : HomeUiState()
}

// UiEvent —— 一次性事件（导航、Snackbar）
sealed class HomeUiEvent {
    data class NavigateTo(val route: String) : HomeUiEvent()
    data class ShowSnackbar(val message: String) : HomeUiEvent()
}

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getItemsUseCase: GetItemsUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    private val _uiEvent = Channel<HomeUiEvent>()
    val uiEvent = _uiEvent.receiveAsFlow()

    init { loadItems() }

    fun loadItems() {
        viewModelScope.launch {
            _uiState.value = HomeUiState.Loading
            getItemsUseCase()
                .onSuccess { _uiState.value = HomeUiState.Success(it) }
                .onFailure { _uiState.value = HomeUiState.Error(it.message ?: "Unknown error") }
        }
    }
}
```

## 仓库模式

```kotlin
// 领域层接口
interface ItemRepository {
    fun observeItems(): Flow<List<Item>>
    suspend fun refreshItems(): Result<Unit>
    suspend fun getItemById(id: String): Result<Item>
}

// 数据层实现
class ItemRepositoryImpl @Inject constructor(
    private val remoteSource: ItemRemoteDataSource,
    private val localSource: ItemLocalDataSource,
    private val mapper: ItemMapper
) : ItemRepository {

    override fun observeItems(): Flow<List<Item>> =
        localSource.observeAll().map { mapper.toDomain(it) }

    override suspend fun refreshItems(): Result<Unit> = runCatching {
        val dto = remoteSource.fetchItems()
        localSource.insertAll(mapper.toEntity(dto))
    }

    override suspend fun getItemById(id: String): Result<Item> = runCatching {
        // 示例实现：从本地缓存获取
        val entity = localSource.getById(id) ?: throw Exception("Item not found")
        mapper.toDomain(entity)
    }
}
```

## Compose 页面

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigate: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }

    // 一次性事件处理
    LaunchedEffect(Unit) {
        viewModel.uiEvent.collect { event ->
            when (event) {
                is HomeUiEvent.NavigateTo -> onNavigate(event.route)
                is HomeUiEvent.ShowSnackbar -> snackbarHostState.showSnackbar(event.message)
            }
        }
    }

    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        when (val state = uiState) {
            is HomeUiState.Loading -> LoadingContent()
            is HomeUiState.Success -> HomeContent(state.items, Modifier.padding(padding))
            is HomeUiState.Error -> ErrorContent(state.message, onRetry = viewModel::loadItems)
        }
    }
}
```

## Room 数据库

```kotlin
@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val title: String,
    val updatedAt: Long = System.currentTimeMillis()
)

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<ItemEntity>>

    @Upsert
    suspend fun upsertAll(items: List<ItemEntity>)

    @Query("DELETE FROM items")
    suspend fun deleteAll()
}

@Database(entities = [ItemEntity::class], version = 1, exportSchema = true)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao
}
```

## Hilt DI 配置

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .client(buildOkHttpClient())
        .build()
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds @Singleton
    abstract fun bindItemRepository(impl: ItemRepositoryImpl): ItemRepository
}
```

## 关键依赖（libs.versions.toml）

```toml
[versions]
kotlin = "2.0.0"
compose-bom = "2024.06.00"
hilt = "2.51"
room = "2.6.1"
retrofit = "2.11.0"
coroutines = "1.8.1"
lifecycle = "2.8.2"

[libraries]
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
compose-ui = { group = "androidx.compose.ui", name = "ui" }
compose-material3 = { group = "androidx.compose.material3", name = "material3" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
```

## 测试配置

```kotlin
// ViewModel 单元测试
@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()

    private val getItemsUseCase = mockk<GetItemsUseCase>()
    private lateinit var viewModel: HomeViewModel

    @BeforeEach
    fun setup() { viewModel = HomeViewModel(getItemsUseCase) }

    @Test
    fun `loadItems emits Success when use case succeeds`() = runTest {
        val items = listOf(Item("1", "Test"))
        coEvery { getItemsUseCase() } returns Result.success(items)

        viewModel.uiState.test {
            skipItems(1) // Loading
            assertThat(awaitItem()).isEqualTo(HomeUiState.Success(items))
        }
    }
}
```