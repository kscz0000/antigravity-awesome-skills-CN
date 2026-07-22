# Kotlin Multiplatform（KMM）参考

## 项目结构

```
project/
├── shared/                          # 共享 KMM 模块
│   ├── src/
│   │   ├── commonMain/kotlin/       # 业务逻辑、领域、数据
│   │   │   ├── domain/
│   │   │   │   ├── model/
│   │   │   │   ├── repository/      # 接口
│   │   │   │   └── usecase/
│   │   │   ├── data/
│   │   │   │   ├── remote/          # Ktor 客户端 + DTO
│   │   │   │   ├── local/           # SQLDelight DAO
│   │   │   │   └── repository/      # 实现
│   │   │   └── di/                  # Koin 模块
│   │   ├── androidMain/kotlin/      # Android 平台相关 actual 实现
│   │   └── iosMain/kotlin/          # iOS 平台相关 actual（如需要）
│   └── build.gradle.kts
├── androidApp/                      # Android 应用模块
│   ├── src/main/java/
│   │   ├── ui/                      # Jetpack Compose 页面
│   │   ├── presentation/            # Android ViewModel
│   │   └── di/                      # Android 平台相关 DI
│   └── build.gradle.kts
└── build.gradle.kts
```

## 共享模块：Ktor HTTP 客户端

```kotlin
// commonMain
expect fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient

// androidMain
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient =
    HttpClient(OkHttp) {
        config(this)
        engine { addInterceptor(/* logging, auth */) }
    }

// 共享调用方式
val client = httpClient {
    install(ContentNegotiation) { json() }
    install(HttpTimeout) { requestTimeoutMillis = 10_000 }
    defaultRequest {
        url(BuildKonfig.BASE_URL)
        header(HttpHeaders.ContentType, ContentType.Application.Json)
    }
}
```

## SQLDelight 配置

```sql
-- ItemEntity.sq
CREATE TABLE ItemEntity (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    updatedAt INTEGER NOT NULL DEFAULT 0
);

selectAll:
SELECT * FROM ItemEntity ORDER BY updatedAt DESC;

upsertItem:
INSERT OR REPLACE INTO ItemEntity (id, title, updatedAt)
VALUES (?, ?, ?);
```

```kotlin
// commonMain —— 数据库驱动的 expect/actual
expect class DatabaseDriverFactory {
    fun createDriver(): SqlDriver
}

// androidMain
actual class DatabaseDriverFactory(private val context: Context) {
    actual fun createDriver(): SqlDriver =
        AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
}
```

## 共享仓库

```kotlin
// commonMain
class ItemRepositoryImpl(
    private val remoteSource: ItemRemoteDataSource,
    private val localSource: ItemLocalDataSource,
) : ItemRepository {

    override fun observeItems(): Flow<List<Item>> =
        localSource.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }

    override suspend fun refreshItems(): Result<Unit> = runCatching {
        val items = remoteSource.fetchItems()
        localSource.upsertAll(items.map { it.toEntity() })
    }
}
```

## Android ViewModel 消费共享 Flow

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val observeItems: ObserveItemsUseCase,    // 来自共享模块
    private val refreshItems: RefreshItemsUseCase     // 来自共享模块
) : ViewModel() {

    val uiState = observeItems()
        .map { HomeUiState.Success(it) as HomeUiState }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = HomeUiState.Loading
        )
}
```

## Koin DI（共享 + Android）

```kotlin
// commonMain —— 共享 Koin 模块
val sharedModule = module {
    single { DatabaseDriverFactory(get()) }
    single { AppDatabase(get<DatabaseDriverFactory>().createDriver()) }
    single<ItemRepository> { ItemRepositoryImpl(get(), get()) }
    factory { ObserveItemsUseCase(get()) }
    factory { RefreshItemsUseCase(get()) }
}

// androidApp —— Android 平台专属模块
val androidModule = module {
    single<Context> { androidApplication() }
    viewModel { HomeViewModel(get(), get()) }
}

// Application 类
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@MyApp)
            modules(sharedModule, androidModule)
        }
    }
}
```

## 关键 Gradle 依赖（shared/build.gradle.kts）

```kotlin
kotlin {
    androidTarget()
    // 根据需要添加其他 target（jvm、iosArm64 等）

    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.ktor.serialization.kotlinx.json)
            implementation(libs.sqldelight.runtime)
            implementation(libs.koin.core)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
            implementation(libs.sqldelight.android.driver)
            implementation(libs.koin.android)
        }
    }
}
```

## Compose Multiplatform（共享 UI）

适用场景：Android + 桌面 + Web 之间共享 UI。

```kotlin
// commonMain —— 共享 Composable
@Composable
fun HomeScreenContent(
    state: HomeUiState,
    onRetry: () -> Unit
) {
    when (state) {
        is HomeUiState.Loading -> CircularProgressIndicator()
        is HomeUiState.Success -> ItemList(state.items)
        is HomeUiState.Error -> ErrorView(state.message, onRetry)
    }
}

// androidApp —— 通过 Android ViewModel 包装
@Composable
fun HomeScreen(viewModel: HomeViewModel = koinViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    HomeScreenContent(state, onRetry = viewModel::refresh)
}
```