# RN 社区库的即插即用替代组件

`@expo/ui` 为流行的 React Native 社区库提供了 API 兼容的替代组件，由原生 `@expo/ui` 组件（Android 上是 Jetpack Compose、iOS 上是 SwiftUI）驱动。当你需要将现有应用从某个社区 UI 依赖迁移出去时可以使用这些替代组件——其 API 与被替换的库一致，因此通常只需修改导入路径即可完成替换。

## 可用的替代组件

每个即插即用替代组件都位于 `@expo/ui/community/<kebab-case-name>`。请注意哪些是默认导入，哪些是命名导入。

| 替代对象 | 导入 |
|----------|--------|
| `@gorhom/bottom-sheet` | `import BottomSheet, { BottomSheetView } from '@expo/ui/community/bottom-sheet'` |
| `@react-native-community/datetimepicker` | `import DateTimePicker from '@expo/ui/community/datetime-picker'` |
| `@react-native-masked-view/masked-view` | `import { MaskedView } from '@expo/ui/community/masked-view'` |
| `@react-native-menu/menu` | `import { MenuView } from '@expo/ui/community/menu'` |
| `react-native-pager-view` | `import PagerView from '@expo/ui/community/pager-view'` |
| `@react-native-picker/picker` | `import { Picker } from '@expo/ui/community/picker'` |
| `@react-native-segmented-control/segmented-control` | `import SegmentedControl from '@expo/ui/community/segmented-control'` |
| `@react-native-community/slider` | `import Slider from '@expo/ui/community/slider'` |

## 确认 API

每个组件都有专属的文档页面，介绍设置和使用方法：

- 概述 — https://docs.expo.dev/versions/latest/sdk/ui/drop-in-replacements/index.md
- 各组件 — https://docs.expo.dev/versions/latest/sdk/ui/drop-in-replacements/{component}/index.md （slug 为组件名小写、无连字符，例如 `bottomsheet`、`datetimepicker`、`segmentedcontrol`）

已安装包的 TypeScript 类型文件（`.d.ts`）是确认你 SDK 版本中确切属性的最可靠真相来源（`@expo/ui` 的版本与 SDK 绑定，其 API 在不同版本之间可能会变化）。请结合文档页面来了解平台支持以及与被替换库有差异的属性。