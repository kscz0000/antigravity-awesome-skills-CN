---
title: "Search fields | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/search-fields

# 搜索字段

搜索字段让用户通过输入特定词语在内容集合中搜索。

![A stylized representation of a search field containing placeholder text and a dictation icon. The image is tinted red to subtly reflect the red in the original six-color Apple logo.](https://docs-assets.developer.apple.com/published/73f9e564b79cbe48e29ae2a9f7b83682/components-search-field-intro%402x.png)

搜索字段是一个可编辑的文本字段，显示搜索图标、清除按钮和占位符文本，用户可在其中输入搜索内容。搜索字段可使用[范围控件](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-controls-and-tokens)和[令牌](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-controls-and-tokens)来帮助过滤和细化搜索范围。各平台根据应用的目标和设计有不同的搜索访问模式。

开发者指南参见 [Adding a search interface to your app](https://developer.apple.com/documentation/SwiftUI/Adding-a-search-interface-to-your-app)；系统级搜索指南参见 [Searching](https://developer.apple.com/design/human-interface-guidelines/searching)。

## [最佳实践](https://developer.apple.com/design/human-interface-guidelines/search-fields#Best-practices)

**显示描述可搜索信息类型的占位符文本。** 例如，Apple TV 应用包含占位符文本"节目、电影及更多内容"。避免使用"搜索"等词语作为占位符文本，因为它不提供有用信息。

**尽可能在用户输入时立即开始搜索。** 边输入边搜索使搜索体验更流畅，因为随着文本变得更具体，结果会持续细化。

**考虑在搜索开始前或用户输入时显示建议搜索词。** 这可以帮助用户更快搜索，即使搜索本身不会立即开始，也能建议常见搜索。

**简化搜索结果。** 优先显示最相关的搜索结果，减少用户滚动查找的需求。除了优先显示最可能的结果，考虑对结果分类以帮助用户找到所需内容。

**考虑让用户过滤搜索结果。** 例如，可以在搜索结果内容区域包含范围控件，帮助用户快速轻松地过滤搜索结果。

## [范围控件和令牌](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-controls-and-tokens)

范围控件和令牌是让用户在搜索前后缩小搜索参数的组件。

  * _范围控件_ 类似[分段控件](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)，用于选择搜索类别。

  * _令牌_ 是搜索词的可视化表示，用户可选择和编辑，并作为搜索中其他词语的过滤器。




![A diagram of the Mail app on iPhone with the search field open above the keyboard and the word Design entered in the field. Callouts indicate a scope control at the top of the screen to switch between searching all mailboxes and the current mailbox, and a list of tokens in a Suggestions area beneath the control that represent different filters for the search.](https://docs-assets.developer.apple.com/published/c39602d60041fae736e46f91641d8373/search-fields-scope-control-tokens%402x.png)

**使用范围控件在明确定义的搜索类别间过滤。** 范围控件可以帮助用户从更宽的范围缩小到更窄的范围。例如，iPhone 上的邮件应用中，范围控件帮助用户从搜索整个邮箱缩小到仅搜索当前查看的邮箱。开发者指南参见 [Scoping a search operation](https://developer.apple.com/documentation/SwiftUI/Scoping-a-search-operation)。

**默认使用更宽的范围，让用户按需细化。** 更宽的范围为完整结果集提供上下文，帮助用户在选择缩小范围时朝有用方向前进。

**使用令牌按常见搜索词或项目过滤。** 定义令牌时，其代表的词语会获得封装它的可视化处理，表明用户可以将其作为单个项目选择和编辑。令牌可以澄清搜索词，如在邮件中按特定联系人过滤，或将搜索聚焦到特定属性集，如在信息中按照片过滤。macOS 相关组件参见 [Token fields](https://developer.apple.com/design/human-interface-guidelines/token-fields)。

**考虑将令牌与搜索建议配对。** 用户可能不知道有哪些令牌可用，因此将它们与搜索建议配对可以帮助用户学习如何使用。

## [平台注意事项](https://developer.apple.com/design/human-interface-guidelines/search-fields#Platform-considerations)

_visionOS 无额外注意事项。_

### [iOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iOS)

搜索入口点有三个主要位置：

  * 屏幕底部的标签栏

  * 屏幕底部或顶部的工具栏

  * 直接内嵌于内容中




搜索的最佳位置取决于应用的布局、内容和导航。

#### [标签栏中的搜索](https://developer.apple.com/design/human-interface-guidelines/search-fields#Search-in-a-tab-bar)

可以将搜索作为视觉上独立的标签放在标签栏的尾端，这样当用户在应用的各部分间切换时，搜索保持可见且始终可用。

![An illustration of a tab bar at the bottom of an iPhone screen. A tab for search appears on the trailing edge in a visually distinct group.](https://docs-assets.developer.apple.com/published/ca6977596a62743265fdd2132616a4c8/search-fields-search-as-tab%402x.png)

当用户导航到搜索标签时，出现的搜索字段可以是_聚焦_或_非聚焦_状态。

![An illustration of an iPhone screen with search in a tab bar at the bottom of the screen. The tab bar is hidden by the keyboard and the search field is open above the keyboard, ready for text entry.](https://docs-assets.developer.apple.com/published/cbd1eb280ecd0f8f71aab784a2bcd042/search-fields-tab-focused%402x.png)

聚焦

![An illustration of an iPhone screen with search in a tab bar at the bottom of the screen. The search tab is expanded into a field that hides the tabs to its leading side. A single remaining tab on the leading edge of the screen indicates that it's possible to navigate away, and the space above the tab bar is empty and available for other content.](https://docs-assets.developer.apple.com/published/196b81213f5131b324f952180a4e9c46/search-fields-tab-unfocused%402x.png)

非聚焦

**以聚焦状态开始搜索字段，帮助用户快速找到所需内容。** 当搜索字段以聚焦状态开始时，键盘立即出现，搜索字段位于其上方，准备开始搜索。这提供了更短暂的体验，用户退出搜索后直接返回之前的标签，适用于希望搜索快速无缝完成的场景。

**以非聚焦状态开始搜索字段，促进发现和探索。** 当搜索字段以非聚焦状态开始时，搜索标签在屏幕底部展开为未选中的字段。这为屏幕其余部分留出空间，用于额外的发现或导航，然后用户点击字段开始搜索。这对于有大量内容要展示的应用很有用，如音乐或电视应用。

#### [工具栏中的搜索](https://developer.apple.com/design/human-interface-guidelines/search-fields#Search-in-a-toolbar)

作为标签栏搜索的替代，也可以将搜索放在屏幕底部或顶部的工具栏中。

  * 可以在底部工具栏中包含搜索，作为展开的字段或工具栏按钮，取决于可用空间和搜索对应用的重要程度。当用户点击时，它会动画展开为键盘上方的搜索字段，准备输入。

  * 可以在顶部工具栏（也称为导航栏）中包含搜索，显示为工具栏按钮。当用户点击时，它会动画展开为搜索字段，显示在键盘上方，或如果底部没有空间则内嵌显示在顶部。




![An illustration of an iPhone screen with search in a bottom toolbar. The search field is positioned in an isolated group between a Filter button on the leading edge and a Compose button on the trailing edge.](https://docs-assets.developer.apple.com/published/face9eed2f9c99f2c12ca3a400919e03/search-fields-ios-toolbar-with-items%402x.png)

底部工具栏中的搜索

![An illustration of an iPhone screen with search in a top toolbar. A Back button appears on the leading edge, and an Add button appears on the trailing edge. An button group with Search and More appears next to the Add button.](https://docs-assets.developer.apple.com/published/ca4d0118cd29bd05bd2fd114163a1f64/search-fields-ios-navigation-bar-item%402x.png)

顶部工具栏中的搜索

**如果有空间，将搜索放在底部。** 可以将搜索字段添加到现有工具栏，或作为新工具栏的唯一项目。底部搜索在任何搜索为优先级的场景中都很有用，因为它保持搜索体验易于触达。在各种工具栏布局中使用底部搜索的应用示例包括设置（搜索是唯一项目）、邮件和备忘录（与其他重要控件并列）。

**当需要让位于屏幕底部的内容或没有底部工具栏时，将搜索放在顶部。** 在覆盖内容可能干扰应用主要功能的场景中使用顶部搜索。例如，钱包应用在屏幕底部以堆叠方式包含活动票券，便于访问和一目了然。

#### [内嵌搜索字段](https://developer.apple.com/design/human-interface-guidelines/search-fields#Search-as-an-inline-field)

某些情况下，可能希望应用包含与内容内嵌的搜索字段。

**当搜索字段与其搜索的内容并列位置能加强这种关系时，将其作为内嵌字段放置。** 当需要在单个视图中过滤或搜索时，让搜索直接出现在内容旁边有助于说明搜索适用于该内容而非全局。例如，虽然音乐应用的主要搜索在标签栏中，但用户可以导航到他们的资料库并使用内嵌搜索字段过滤歌曲和专辑。

**优先将搜索放在底部。** 通常，即使对于应用于应用内容子集的搜索，最好将搜索放在用户易于触达的位置。例如，设置应用在顶部搜索和各个应用的设置部分搜索都将搜索放在底部。如果底部没有空间（例如被标签栏或其他重要 UI 占用），可以将搜索内嵌放在顶部。

**当在顶部时，将内嵌搜索字段放在其搜索的列表上方，滚动时固定在顶部工具栏。** 这有助于将其与其他位置出现的搜索区分开。

### [iPadOS, macOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iPadOS-macOS)

iPadOS 和 macOS 中搜索字段的位置和行为类似；在两个平台上，清除字段会退出搜索并关闭键盘（如果存在）。如果应用同时在 iPad 和 Mac 上可用，尽量在两个平台上保持搜索体验一致。

![An illustration of an iPad screen with a search field on the trailing edge of the top toolbar. The search field has the word Design entered into the field, and three search suggestions appear in a list beneath the field. The toolbar also includes an Inspector button, a group with New Folder and Favorite buttons, and a Share button next to the search field.](https://docs-assets.developer.apple.com/published/368ba21a44b4c65a4e53d3d2197d061b/search-fields-toolbar-search-ipad%402x.png)iPadOS

![An illustration of a Mac screen with a search field on the trailing edge of the toolbar. The search field has the word Design entered into the field, and three search suggestions appear in a list beneath the field. The toolbar also includes an Inspector button, a group with New Folder and Favorite buttons, and a Share button next to the search field.](https://docs-assets.developer.apple.com/published/eb1970b09f7b35b39757201a31289bc3/search-fields-toolbar-search-mac%402x.png)macOS

**将搜索字段放在工具栏尾端，适用于大多数常见场景。** 许多应用受益于工具栏中搜索的熟悉模式，特别是具有分栏视图或在多个来源间导航的应用，如邮件、备忘录和语音备忘录。搜索在工具栏侧边的持续可用性使其在应用内具有全局存在感，因此通常适合以全局范围开始初始搜索。

**在侧边栏顶部包含搜索，用于过滤内容或导航。** 设置等应用利用搜索快速过滤侧边栏，暴露可能深达多级的部分，为用户提供搜索、预览和导航到所需部分或设置的简单方式。

![An illustration of an iPad screen with a search field at the top of the sidebar on the leading edge of the screen.](https://docs-assets.developer.apple.com/published/8aed61a23fe2a9885d1a1d1da15a4b09/search-fields-ipad-search-in-sidebar%402x.png)

**当需要专门的发现区域时，将搜索作为侧边栏或标签栏中的项目包含。** 如果搜索配有丰富的建议、类别或需要更多空间的内容，为其提供专门区域会有帮助。这对于浏览和搜索并行的应用尤其如此，如音乐和电视应用，它提供了突出显示建议内容、类别和最近搜索的统一位置。专门区域还确保搜索在用户导航和切换应用各部分时始终可用。

![An illustration of an iPad screen with a tab bar at the top edge. The trailing side of the tab bar includes a Search tab with a distinct background color to differentiate it from other tab areas.](https://docs-assets.developer.apple.com/published/a2ab9bc29018fc1bbc604a91dfc905c7/search-fields-ipad-search-in-tab-bar%402x.png)

**在专门区域的搜索字段中，考虑当用户导航到该部分时立即聚焦字段，帮助用户更快搜索并更容易定位字段本身。** 例外情况是 iPad 上只有虚拟键盘可用时，此时最好让字段保持非聚焦状态，以防止键盘意外覆盖视图。

**考虑搜索字段位置对窗口调整大小的适应。** 在 iPad 上，搜索字段像 Mac 一样随应用窗口流畅调整大小。然而，对于 iPad 上的紧凑视图，确保搜索在上下文最有用的位置可用很重要。例如，备忘录和邮件在调整到紧凑视图时，将搜索放在内容列表列的上方。

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#tvOS)

搜索屏幕是一个专门的键盘屏幕，帮助用户输入搜索文本，在键盘下方以完全可自定义的视图显示搜索结果。开发者指南参见 [`UISearchController`](https://developer.apple.com/documentation/UIKit/UISearchController)。

![An illustration of a search screen in tvOS. The screen includes a field with a keyboard input area at the top, a scope control, and a grid of top results at the bottom.](https://docs-assets.developer.apple.com/published/590a4ef7b02ccd9758f0e52e5c261574/search-fields-tvos-search%402x.png)

**提供建议使搜索更容易。** 用户通常不想在 tvOS 中输入大量文字。为改善搜索体验，提供热门和上下文相关的搜索建议，包括可用的最近搜索。开发者指南参见 [Using suggested searches with a search controller](https://developer.apple.com/documentation/UIKit/using-suggested-searches-with-a-search-controller)。

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#watchOS)

当用户点击搜索字段时，系统显示覆盖整个屏幕的文本输入控件。应用仅在用户点击取消或搜索按钮后才返回搜索字段。

## [资源](https://developer.apple.com/design/human-interface-guidelines/search-fields#Resources)

#### [相关](https://developer.apple.com/design/human-interface-guidelines/search-fields#Related)

[Searching](https://developer.apple.com/design/human-interface-guidelines/searching)

[Token fields](https://developer.apple.com/design/human-interface-guidelines/token-fields)

#### [开发者文档](https://developer.apple.com/design/human-interface-guidelines/search-fields#Developer-documentation)

[Adding a search interface to your app](https://developer.apple.com/documentation/SwiftUI/Adding-a-search-interface-to-your-app) — SwiftUI

[`searchable(text:placement:prompt:)`](https://developer.apple.com/documentation/SwiftUI/View/searchable\(text:placement:prompt:\)) — SwiftUI

[`UISearchBar`](https://developer.apple.com/documentation/UIKit/UISearchBar) — UIKit

[`UISearchTextField`](https://developer.apple.com/documentation/UIKit/UISearchTextField) — UIKit

[`NSSearchField`](https://developer.apple.com/documentation/AppKit/NSSearchField) — AppKit

#### [视频](https://developer.apple.com/design/human-interface-guidelines/search-fields#Videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/3055294D-836B-4513-B7B0-0BC5666246B0/1AAA030E-2ECA-47D8-AE09-6D7B72A840F6/10044_wide_250x141_1x.jpg) Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/BE8FF113-0FE1-40FC-86BF-FE95BE2FF7A5/5027_wide_250x141_1x.jpg) Discoverable design ](https://developer.apple.com/videos/play/wwdc2021/10126)

[![](https://devimages-cdn.apple.com/wwdc-services/images/119/D45C244B-2038-4692-99A0-6131ED5FD984/5084_wide_250x141_1x.jpg) Craft search experiences in SwiftUI ](https://developer.apple.com/videos/play/wwdc2021/10176)

## [变更日志](https://developer.apple.com/design/human-interface-guidelines/search-fields#Change-log)

日期| 变更
---|---
2025年6月9日| 更新了 iOS 中搜索位置的指南，合并了 iPadOS 和 macOS 平台注意事项，并添加了令牌指南。
2023年9月12日| 合并了所有平台通用的指南。
2023年6月5日| 添加了在 watchOS 中使用搜索字段的指南。
