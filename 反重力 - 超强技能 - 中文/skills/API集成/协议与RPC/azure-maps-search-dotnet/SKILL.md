---
name: azure-maps-search-dotnet
description: Azure Maps .NET SDK。基于位置的服务，包括地理编码、路径规划、地图渲染、地理定位和天气。当用户要求'地址搜索、路线规划、地图瓦片、IP地理定位、天气数据查询'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Maps (.NET)

Azure Maps .NET SDK，提供基于位置的服务：地理编码、路径规划、地图渲染、地理定位和天气。

## 安装

```bash
# Search (geocoding, reverse geocoding)
dotnet add package Azure.Maps.Search --prerelease

# Routing (directions, route matrix)
dotnet add package Azure.Maps.Routing --prerelease

# Rendering (map tiles, static images)
dotnet add package Azure.Maps.Rendering --prerelease

# Geolocation (IP to location)
dotnet add package Azure.Maps.Geolocation --prerelease

# Weather
dotnet add package Azure.Maps.Weather --prerelease

# Resource Management (account management, SAS tokens)
dotnet add package Azure.ResourceManager.Maps --prerelease

# Required for authentication
dotnet add package Azure.Identity
```

**当前版本**：
- `Azure.Maps.Search`: v2.0.0-beta.5
- `Azure.Maps.Routing`: v1.0.0-beta.4
- `Azure.Maps.Rendering`: v2.0.0-beta.1
- `Azure.Maps.Geolocation`: v1.0.0-beta.3
- `Azure.ResourceManager.Maps`: v1.1.0-beta.2

## 环境变量

```bash
AZURE_MAPS_SUBSCRIPTION_KEY=<your-subscription-key>
AZURE_MAPS_CLIENT_ID=<your-client-id>  # For Entra ID auth
```

## 身份验证

### 订阅密钥（共享密钥）

```csharp
using Azure;
using Azure.Maps.Search;

var subscriptionKey = Environment.GetEnvironmentVariable("AZURE_MAPS_SUBSCRIPTION_KEY");
var credential = new AzureKeyCredential(subscriptionKey);

var client = new MapsSearchClient(credential);
```

### Microsoft Entra ID（生产环境推荐）

```csharp
using Azure.Identity;
using Azure.Maps.Search;

var credential = new DefaultAzureCredential();
var clientId = Environment.GetEnvironmentVariable("AZURE_MAPS_CLIENT_ID");

var client = new MapsSearchClient(credential, clientId);
```

### 共享访问签名（SAS）

```csharp
using Azure;
using Azure.Core;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Maps;
using Azure.ResourceManager.Maps.Models;
using Azure.Maps.Search;

// Authenticate with Azure Resource Manager
ArmClient armClient = new ArmClient(new DefaultAzureCredential());

// Get Maps account resource
ResourceIdentifier mapsAccountResourceId = MapsAccountResource.CreateResourceIdentifier(
    subscriptionId, resourceGroupName, accountName);
MapsAccountResource mapsAccount = armClient.GetMapsAccountResource(mapsAccountResourceId);

// Generate SAS token
MapsAccountSasContent sasContent = new MapsAccountSasContent(
    MapsSigningKey.PrimaryKey, 
    principalId, 
    maxRatePerSecond: 500, 
    start: DateTime.UtcNow.ToString("O"), 
    expiry: DateTime.UtcNow.AddDays(1).ToString("O"));

Response<MapsAccountSasToken> sas = mapsAccount.GetSas(sasContent);

// Create client with SAS token
var sasCredential = new AzureSasCredential(sas.Value.AccountSasToken);
var client = new MapsSearchClient(sasCredential);
```

## 客户端层级

```
Azure.Maps.Search
└── MapsSearchClient
    ├── GetGeocoding()                    → Geocode addresses
    ├── GetGeocodingBatch()               → Batch geocoding
    ├── GetReverseGeocoding()             → Coordinates to address
    ├── GetReverseGeocodingBatch()        → Batch reverse geocoding
    └── GetPolygon()                      → Get boundary polygons

Azure.Maps.Routing
└── MapsRoutingClient
    ├── GetDirections()                   → Route directions
    ├── GetImmediateRouteMatrix()         → Route matrix (sync, ≤100)
    ├── GetRouteMatrix()                  → Route matrix (async, ≤700)
    └── GetRouteRange()                   → Isochrone/reachable range

Azure.Maps.Rendering
└── MapsRenderingClient
    ├── GetMapTile()                      → Map tiles
    ├── GetMapStaticImage()               → Static map images
    └── GetCopyrightCaption()             → Copyright info

Azure.Maps.Geolocation
└── MapsGeolocationClient
    └── GetCountryCode()                  → IP to country/region

Azure.Maps.Weather
└── MapsWeatherClient
    ├── GetCurrentWeatherConditions()     → Current weather
    ├── GetDailyForecast()                → Daily forecast
    ├── GetHourlyForecast()               → Hourly forecast
    └── GetSevereWeatherAlerts()          → Weather alerts
```

## 核心工作流

### 1. 地理编码（地址转坐标）

```csharp
using Azure;
using Azure.Maps.Search;

var credential = new AzureKeyCredential(subscriptionKey);
var client = new MapsSearchClient(credential);

Response<GeocodingResponse> result = client.GetGeocoding("1 Microsoft Way, Redmond, WA 98052");

foreach (var feature in result.Value.Features)
{
    Console.WriteLine($"Coordinates: {string.Join(",", feature.Geometry.Coordinates)}");
    Console.WriteLine($"Address: {feature.Properties.Address.FormattedAddress}");
    Console.WriteLine($"Confidence: {feature.Properties.Confidence}");
}
```

### 2. 批量地理编码

```csharp
using Azure.Maps.Search.Models.Queries;

List<GeocodingQuery> queries = new List<GeocodingQuery>
{
    new GeocodingQuery() { Query = "400 Broad St, Seattle, WA" },
    new GeocodingQuery() { Query = "1 Microsoft Way, Redmond, WA" },
    new GeocodingQuery() { AddressLine = "Space Needle", Top = 1 },
};

Response<GeocodingBatchResponse> results = client.GetGeocodingBatch(queries);

foreach (var batchItem in results.Value.BatchItems)
{
    foreach (var feature in batchItem.Features)
    {
        Console.WriteLine($"Coordinates: {string.Join(",", feature.Geometry.Coordinates)}");
    }
}
```

### 3. 逆地理编码（坐标转地址）

```csharp
using Azure.Core.GeoJson;

GeoPosition coordinates = new GeoPosition(-122.138685, 47.6305637);
Response<GeocodingResponse> result = client.GetReverseGeocoding(coordinates);

foreach (var feature in result.Value.Features)
{
    Console.WriteLine($"Address: {feature.Properties.Address.FormattedAddress}");
    Console.WriteLine($"Locality: {feature.Properties.Address.Locality}");
}
```

### 4. 获取边界多边形

```csharp
using Azure.Maps.Search.Models;

GetPolygonOptions options = new GetPolygonOptions()
{
    Coordinates = new GeoPosition(-122.204141, 47.61256),
    ResultType = BoundaryResultTypeEnum.Locality,
    Resolution = ResolutionEnum.Small,
};

Response<Boundary> result = client.GetPolygon(options);

Console.WriteLine($"Boundary copyright: {result.Value.Properties?.Copyright}");
Console.WriteLine($"Polygon count: {result.Value.Geometry.Count}");
```

### 5. 路线方向

```csharp
using Azure;
using Azure.Core.GeoJson;
using Azure.Maps.Routing;
using Azure.Maps.Routing.Models;

var client = new MapsRoutingClient(new AzureKeyCredential(subscriptionKey));

List<GeoPosition> routePoints = new List<GeoPosition>()
{
    new GeoPosition(-122.34, 47.61),  // Seattle
    new GeoPosition(-122.13, 47.64)   // Redmond
};

RouteDirectionQuery query = new RouteDirectionQuery(routePoints);
Response<RouteDirections> result = client.GetDirections(query);

foreach (var route in result.Value.Routes)
{
    Console.WriteLine($"Distance: {route.Summary.LengthInMeters} meters");
    Console.WriteLine($"Duration: {route.Summary.TravelTimeDuration}");
    
    foreach (RouteLeg leg in route.Legs)
    {
        Console.WriteLine($"Leg points: {leg.Points.Count}");
    }
}
```

### 6. 带选项的路线方向

```csharp
RouteDirectionOptions options = new RouteDirectionOptions()
{
    RouteType = RouteType.Fastest,
    UseTrafficData = true,
    TravelMode = TravelMode.Bicycle,
    Language = RoutingLanguage.EnglishUsa,
    InstructionsType = RouteInstructionsType.Text,
};

RouteDirectionQuery query = new RouteDirectionQuery(routePoints)
{
    RouteDirectionOptions = options
};

Response<RouteDirections> result = client.GetDirections(query);
```

### 7. 路线矩阵

```csharp
RouteMatrixQuery routeMatrixQuery = new RouteMatrixQuery
{
    Origins = new List<GeoPosition>()
    {
        new GeoPosition(-122.34, 47.61),
        new GeoPosition(-122.13, 47.64)
    },
    Destinations = new List<GeoPosition>() 
    { 
        new GeoPosition(-122.20, 47.62),
        new GeoPosition(-122.40, 47.65)
    },
};

// Synchronous (up to 100 route combinations)
Response<RouteMatrixResult> result = client.GetImmediateRouteMatrix(routeMatrixQuery);

foreach (var cell in result.Value.Matrix.SelectMany(row => row))
{
    Console.WriteLine($"Distance: {cell.Response?.RouteSummary?.LengthInMeters}");
    Console.WriteLine($"Duration: {cell.Response?.RouteSummary?.TravelTimeDuration}");
}

// Asynchronous (up to 700 route combinations)
RouteMatrixOptions routeMatrixOptions = new RouteMatrixOptions(routeMatrixQuery)
{
    TravelTimeType = TravelTimeType.All,
};
GetRouteMatrixOperation asyncResult = client.GetRouteMatrix(WaitUntil.Completed, routeMatrixOptions);
```

### 8. 路线范围（等时线）

```csharp
RouteRangeOptions options = new RouteRangeOptions(-122.34, 47.61)
{
    TimeBudget = new TimeSpan(0, 20, 0)  // 20 minutes
};

Response<RouteRangeResult> result = client.GetRouteRange(options);

// result.Value.ReachableRange contains the polygon
Console.WriteLine($"Boundary points: {result.Value.ReachableRange.Boundary.Count}");
```

### 9. 获取地图瓦片

```csharp
using Azure;
using Azure.Maps.Rendering;

var client = new MapsRenderingClient(new AzureKeyCredential(subscriptionKey));

int zoom = 10;
int tileSize = 256;

// Convert coordinates to tile index
MapTileIndex tileIndex = MapsRenderingClient.PositionToTileXY(
    new GeoPosition(13.3854, 52.517), zoom, tileSize);

// Fetch map tile
GetMapTileOptions options = new GetMapTileOptions(
    MapTileSetId.MicrosoftImagery,
    new MapTileIndex(tileIndex.X, tileIndex.Y, zoom)
);

Response<Stream> mapTile = client.GetMapTile(options);

// Save to file
using (FileStream fileStream = File.Create("./MapTile.png"))
{
    mapTile.Value.CopyTo(fileStream);
}
```

### 10. IP 地理定位

```csharp
using System.Net;
using Azure;
using Azure.Maps.Geolocation;

var client = new MapsGeolocationClient(new AzureKeyCredential(subscriptionKey));

IPAddress ipAddress = IPAddress.Parse("2001:4898:80e8:b::189");
Response<CountryRegionResult> result = client.GetCountryCode(ipAddress);

Console.WriteLine($"Country ISO Code: {result.Value.IsoCode}");
```

### 11. 当前天气

```csharp
using Azure;
using Azure.Core.GeoJson;
using Azure.Maps.Weather;

var client = new MapsWeatherClient(new AzureKeyCredential(subscriptionKey));

var position = new GeoPosition(-122.13071, 47.64011);
var options = new GetCurrentWeatherConditionsOptions(position);

Response<CurrentConditionsResult> result = client.GetCurrentWeatherConditions(options);

foreach (var condition in result.Value.Results)
{
    Console.WriteLine($"Temperature: {condition.Temperature.Value} {condition.Temperature.Unit}");
    Console.WriteLine($"Weather: {condition.Phrase}");
    Console.WriteLine($"Humidity: {condition.RelativeHumidity}%");
}
```

## 关键类型参考

### Search 包

| 类型 | 用途 |
|------|------|
| `MapsSearchClient` | 搜索操作的主客户端 |
| `GeocodingResponse` | 地理编码结果 |
| `GeocodingBatchResponse` | 批量地理编码结果 |
| `GeocodingQuery` | 批量地理编码查询 |
| `ReverseGeocodingQuery` | 批量逆地理编码查询 |
| `GetPolygonOptions` | 多边形检索选项 |
| `Boundary` | 边界多边形结果 |
| `BoundaryResultTypeEnum` | 边界类型（Locality、AdminDistrict 等） |
| `ResolutionEnum` | 多边形分辨率（Small、Medium、Large） |

### Routing 包

| 类型 | 用途 |
|------|------|
| `MapsRoutingClient` | 路径规划操作的主客户端 |
| `RouteDirectionQuery` | 路线方向查询 |
| `RouteDirectionOptions` | 路线计算选项 |
| `RouteDirections` | 路线方向结果 |
| `RouteLeg` | 路线段 |
| `RouteMatrixQuery` | 路线矩阵查询 |
| `RouteMatrixResult` | 路线矩阵结果 |
| `RouteRangeOptions` | 等时线选项 |
| `RouteRangeResult` | 等时线结果 |
| `RouteType` | 路线类型（Fastest、Shortest、Eco、Thrilling） |
| `TravelMode` | 出行方式（Car、Truck、Bicycle、Pedestrian） |

### Rendering 包

| 类型 | 用途 |
|------|------|
| `MapsRenderingClient` | 渲染操作的主客户端 |
| `GetMapTileOptions` | 地图瓦片选项 |
| `MapTileIndex` | 瓦片坐标（X、Y、Zoom） |
| `MapTileSetId` | 瓦片集标识符 |

### 通用类型

| 类型 | 用途 |
|------|------|
| `GeoPosition` | 地理位置坐标（经度、纬度） |
| `GeoBoundingBox` | 地理区域边界框 |

## 最佳实践

1. **生产环境使用 Entra ID** — 优先于订阅密钥
2. **批量操作** — 多个地址使用批量地理编码
3. **缓存结果** — 地理编码结果不常变化
4. **选择合适的瓦片尺寸** — 根据显示需求选择 256 或 512 像素
5. **处理速率限制** — 实现指数退避策略
6. **使用异步路线矩阵** — 大规模矩阵计算（>100）时使用
7. **考虑交通数据** — 设置 `UseTrafficData = true` 以获取准确的预计到达时间

## 错误处理

```csharp
try
{
    Response<GeocodingResponse> result = client.GetGeocoding(address);
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Status: {ex.Status}");
    Console.WriteLine($"Error: {ex.Message}");
    
    switch (ex.Status)
    {
        case 400:
            // Invalid request parameters
            break;
        case 401:
            // Authentication failed
            break;
        case 429:
            // Rate limited - implement backoff
            break;
    }
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.Maps.Search` | 地理编码、搜索 | `dotnet add package Azure.Maps.Search --prerelease` |
| `Azure.Maps.Routing` | 路线方向、矩阵 | `dotnet add package Azure.Maps.Routing --prerelease` |
| `Azure.Maps.Rendering` | 地图瓦片、图像 | `dotnet add package Azure.Maps.Rendering --prerelease` |
| `Azure.Maps.Geolocation` | IP 地理定位 | `dotnet add package Azure.Maps.Geolocation --prerelease` |
| `Azure.Maps.Weather` | 天气数据 | `dotnet add package Azure.Maps.Weather --prerelease` |
| `Azure.ResourceManager.Maps` | 账户管理 | `dotnet add package Azure.ResourceManager.Maps --prerelease` |

## 参考链接

| 资源 | URL |
|------|-----|
| Azure Maps 文档 | https://learn.microsoft.com/azure/azure-maps/ |
| Search API 参考 | https://learn.microsoft.com/dotnet/api/azure.maps.search |
| Routing API 参考 | https://learn.microsoft.com/dotnet/api/azure.maps.routing |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/maps |
| 定价 | https://azure.microsoft.com/pricing/details/azure-maps/ |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
