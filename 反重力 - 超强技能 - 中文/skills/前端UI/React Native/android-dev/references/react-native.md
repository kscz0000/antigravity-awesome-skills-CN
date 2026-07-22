# React Native 参考（TypeScript）

## 项目结构

```
src/
├── app/
│   ├── App.tsx                  # 根组件、Provider
│   ├── navigation/              # React Navigation 栈与类型
│   └── store/                   # RTK store 配置
├── features/
│   └── home/
│       ├── api/                 # RTK Query 端点
│       ├── components/          # 页面专属组件
│       ├── hooks/               # 功能级自定义 Hook
│       ├── screens/             # 页面组件
│       ├── store/               # Zustand slice 或 RTK slice
│       └── types.ts             # 功能类型
├── shared/
│   ├── components/              # 设计系统组件
│   ├── hooks/                   # 共享 Hook
│   ├── theme/                   # 颜色、字号、间距常量
│   └── utils/                   # 工具函数
└── services/
    ├── api/                     # Axios/fetch 客户端 + 拦截器
    └── storage/                 # MMKV 封装
```

## 导航配置（React Navigation v7）

```typescript
export type RootStackParamList = {
  Auth: undefined;
  Home: undefined;
  Detail: { id: string };
  Settings: undefined;
};

export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;

const Stack = createNativeStackNavigator<RootStackParamList>();

export const RootNavigator = () => {
  const isLoggedIn = useAuthStore((s) => s.isLoggedIn);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isLoggedIn ? (
        <>
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Detail" component={DetailScreen} />
        </>
      ) : (
        <Stack.Screen name="Auth" component={AuthScreen} />
      )}
    </Stack.Navigator>
  );
};
```

## 状态管理（Zustand + React Query）

```typescript
// 客户端状态 —— Zustand
// 不要将 bearer 或 refresh 令牌持久化到 AsyncStorage 或普通 MMKV。
// 使用平台级的安全模块（如 react-native-keychain 或 expo-secure-store）
// 存储密钥，仅在此处持久化非敏感的 UI 状态。
interface AuthState {
  isLoggedIn: boolean;
  setLoggedIn: (value: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isLoggedIn: false,
      setLoggedIn: (value) => set({ isLoggedIn: value }),
      logout: () => set({ isLoggedIn: false }),
    }),
    { name: 'auth-ui-storage', storage: createJSONStorage(() => mmkvStorage) }
  )
);

// 令牌保存在持久化的应用状态之外。
const getSecureToken = () => Keychain.getGenericPassword().then((r) => (r ? r.password : null));
const saveSecureToken = (token: string) => Keychain.setGenericPassword('auth', token);
const clearSecureToken = () => Keychain.resetGenericPassword();

// 服务端状态 —— React Query
export const useItems = () =>
  useQuery({
    queryKey: ['items'],
    queryFn: itemsApi.getAll,
    staleTime: 5 * 60 * 1000, // 5 分钟
  });

export const useRefreshItems = () =>
  useMutation({
    mutationFn: itemsApi.refresh,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['items'] }),
  });
```

## 页面模式

```typescript
type HomeScreenProps = RootStackScreenProps<'Home'>;

export const HomeScreen: FC<HomeScreenProps> = ({ navigation }) => {
  const { data: items, isLoading, isError, refetch } = useItems();

  if (isLoading) return <LoadingView />;
  if (isError) return <ErrorView onRetry={refetch} />;

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <ItemCard
            item={item}
            onPress={() => navigation.navigate('Detail', { id: item.id })}
          />
        )}
        ListEmptyComponent={<EmptyView />}
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={refetch} />
        }
      />
    </SafeAreaView>
  );
};
```

## API 客户端（带拦截器的 Axios）

```typescript
const apiClient = axios.create({
  baseURL: Config.API_BASE_URL,
  timeout: 10_000,
  headers: { 'Content-Type': 'application/json' },
});

// 鉴权令牌注入
apiClient.interceptors.request.use(async (config) => {
  const token = await getSecureToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// 401 时刷新令牌
apiClient.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      const newToken = await refreshToken();
      if (newToken) {
        await saveSecureToken(newToken);
        useAuthStore.getState().setLoggedIn(true);
        return apiClient(error.config!);
      }
      await clearSecureToken();
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
```

## API 响应校验（Zod）

```typescript
const ItemSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().optional(),
  createdAt: z.string().datetime(),
});

const ItemsResponseSchema = z.array(ItemSchema);
type Item = z.infer<typeof ItemSchema>;

const getItems = async (): Promise<Item[]> => {
  const { data } = await apiClient.get('/items');
  return ItemsResponseSchema.parse(data); // 形状不合法时抛出 ZodError
};
```

## 关键依赖

```json
{
  "dependencies": {
    "react-native": "0.74.x",
    "@react-navigation/native": "^7.0.0",
    "@react-navigation/native-stack": "^7.0.0",
    "@tanstack/react-query": "^5.45.0",
    "zustand": "^4.5.4",
    "axios": "^1.7.2",
    "zod": "^3.23.8",
    "react-native-keychain": "^8.2.0",
    "react-native-mmkv": "^2.12.2",
    "react-native-safe-area-context": "^4.10.1",
    "react-native-screens": "^3.32.0"
  },
  "devDependencies": {
    "typescript": "^5.4.5",
    "@testing-library/react-native": "^12.5.1",
    "msw": "^2.3.1",
    "jest": "^29.7.0"
  }
}
```

## 新架构（Bridgeless）说明
- 在 `android/gradle.properties` 中启用新架构：`newArchEnabled=true`
- 原生模块使用 TurboModules；避免旧版 NativeModules API
- 自定义原生视图使用 Fabric
- 始终启用 Hermes JS 引擎进行测试

## 性能要点
- 在 `renderItem` 与列表项组件上使用 `useCallback` + `memo`
- 调整 `FlatList` 的 `windowSize`、`initialNumToRender`、`maxToRenderPerBatch`
- 避免 JSX 中出现匿名内联函数
- 导航后的大量工作使用 `InteractionManager.runAfterInteractions`
- 使用 `react-native-reanimated` 实现 60fps 动画（运行在 UI 线程）

## 测试

```typescript
describe('HomeScreen', () => {
  it('shows items when query succeeds', async () => {
    server.use(
      http.get(`${API_URL}/items`, () =>
        HttpResponse.json([{ id: '1', title: 'Test Item' }])
      )
    );

    const { getByText } = render(
      <QueryClientProvider client={testQueryClient}>
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      </QueryClientProvider>
    );

    expect(await findByText('Test Item')).toBeTruthy();
  });
});
```