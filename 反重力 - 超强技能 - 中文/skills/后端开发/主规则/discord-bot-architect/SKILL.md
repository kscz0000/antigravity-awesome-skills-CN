---
name: discord-bot-architect
description: 构建生产级 Discord 机器人的专业技能。涵盖 Discord.js (JavaScript) 和 Pycord (Python)、Gateway Intents、斜杠命令、交互组件、速率限制和分片。当用户要求构建 Discord 机器人、开发 Discord Bot、实现斜杠命令、处理 Discord 交互组件时使用。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Discord Bot Architect

构建生产级 Discord 机器人的专业技能。
涵盖 Discord.js (JavaScript) 和 Pycord (Python)、Gateway Intents、斜杠命令、交互组件、速率限制和分片。

## 原则

- 优先使用斜杠命令而非消息解析（Message Content Intent 已弃用）
- 始终在 3 秒内确认交互
- 仅请求必需的 intents（最小化特权 intents）
- 使用指数退避优雅处理速率限制
- 从一开始就规划分片（2500+ 服务器时必需）
- 使用组件（按钮、选择菜单、模态框）实现丰富 UX
- 先用公会命令测试，准备好后部署全局命令

## 模式

### Discord.js v14 基础

使用 Discord.js v14 和斜杠命令的现代 Discord 机器人设置

**何时使用**: 使用 JavaScript/TypeScript 构建 Discord 机器人、需要完整 Gateway 连接和事件、构建复杂交互的机器人

```javascript
// src/index.js
const { Client, Collection, GatewayIntentBits, Events } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
require('dotenv').config();

// Create client with minimal required intents
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    // Add only what you need:
    // GatewayIntentBits.GuildMessages,
    // GatewayIntentBits.MessageContent,  // PRIVILEGED - avoid if possible
  ]
});

// Load commands
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(f => f.endsWith('.js'));

for (const file of commandFiles) {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  if ('data' in command && 'execute' in command) {
    client.commands.set(command.data.name, command);
  }
}

// Load events
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(f => f.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args));
  } else {
    client.on(event.name, (...args) => event.execute(...args));
  }
}

client.login(process.env.DISCORD_TOKEN);
```

```javascript
// src/commands/ping.js
const { SlashCommandBuilder } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Replies with Pong!'),

  async execute(interaction) {
    const sent = await interaction.reply({
      content: 'Pinging...',
      fetchReply: true
    });

    const latency = sent.createdTimestamp - interaction.createdTimestamp;
    await interaction.editReply(`Pong! Latency: ${latency}ms`);
  }
};
```

```javascript
// src/events/interactionCreate.js
const { Events } = require('discord.js');

module.exports = {
  name: Events.InteractionCreate,
  async execute(interaction) {
    if (!interaction.isChatInputCommand()) return;

    const command = interaction.client.commands.get(interaction.commandName);
    if (!command) {
      console.error(`No command matching ${interaction.commandName}`);
      return;
    }

    try {
      await command.execute(interaction);
    } catch (error) {
      console.error(error);
      const reply = {
        content: 'There was an error executing this command!',
        ephemeral: true
      };

      if (interaction.replied || interaction.deferred) {
        await interaction.followUp(reply);
      } else {
        await interaction.reply(reply);
      }
    }
  }
};
```

```javascript
// src/deploy-commands.js
const { REST, Routes } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
require('dotenv').config();

const commands = [];
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(f => f.endsWith('.js'));

for (const file of commandFiles) {
  const command = require(path.join(commandsPath, file));
  commands.push(command.data.toJSON());
}

const rest = new REST().setToken(process.env.DISCORD_TOKEN);

(async () => {
  try {
    console.log(`Refreshing ${commands.length} commands...`);

    // Guild commands (instant, for testing)
    // const data = await rest.put(
    //   Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
    //   { body: commands }
    // );

    // Global commands (can take up to 1 hour to propagate)
    const data = await rest.put(
      Routes.applicationCommands(process.env.CLIENT_ID),
      { body: commands }
    );

    console.log(`Successfully registered ${data.length} commands`);
  } catch (error) {
    console.error(error);
  }
})();
```

### 结构

discord-bot/
├── src/
│   ├── index.js           # Main entry point
│   ├── deploy-commands.js # Command registration script
│   ├── commands/          # Slash command handlers
│   │   └── ping.js
│   └── events/            # Event handlers
│       ├── ready.js
│       └── interactionCreate.js
├── .env
└── package.json

### Pycord 机器人基础

使用 Pycord (Python) 和应用命令的 Discord 机器人

**何时使用**: 使用 Python 构建 Discord 机器人、偏好 async/await 模式、需要良好的斜杠命令支持

```python
# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Configure intents - only enable what you need
intents = discord.Intents.default()
# intents.message_content = True  # PRIVILEGED - avoid if possible
# intents.members = True          # PRIVILEGED

bot = commands.Bot(
    command_prefix="!",  # Legacy, prefer slash commands
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Sync commands (do this carefully - see sharp edges)
    # await bot.sync_commands()

# Slash command
@bot.slash_command(name="ping", description="Check bot latency")
async def ping(ctx: discord.ApplicationContext):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Pong! Latency: {latency}ms")

# Slash command with options
@bot.slash_command(name="greet", description="Greet a user")
async def greet(
    ctx: discord.ApplicationContext,
    user: discord.Option(discord.Member, "User to greet"),
    message: discord.Option(str, "Custom message", required=False)
):
    msg = message or "Hello!"
    await ctx.respond(f"{user.mention}, {msg}")

# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ["DISCORD_TOKEN"])
```

```python
# cogs/general.py
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="info", description="Bot information")
    async def info(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Bot Info",
            description="A helpful Discord bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Requires Members intent (PRIVILEGED)
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"Welcome {member.mention}!")

def setup(bot):
    bot.add_cog(General(bot))
```

### 结构

discord-bot/
├── main.py           # Main bot file
├── cogs/             # Command groups
│   └── general.py
├── .env
└── requirements.txt

### 交互组件模式

使用按钮、选择菜单和模态框实现丰富 UX

**何时使用**: 需要交互式用户界面、收集超出斜杠命令选项的用户输入、构建菜单、确认对话框或表单

```javascript
// Discord.js - Buttons and Select Menus
const {
  SlashCommandBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  StringSelectMenuBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle
} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('menu')
    .setDescription('Shows an interactive menu'),

  async execute(interaction) {
    // Button row
    const buttonRow = new ActionRowBuilder()
      .addComponents(
        new ButtonBuilder()
          .setCustomId('confirm')
          .setLabel('Confirm')
          .setStyle(ButtonStyle.Primary),
        new ButtonBuilder()
          .setCustomId('cancel')
          .setLabel('Cancel')
          .setStyle(ButtonStyle.Danger),
        new ButtonBuilder()
          .setLabel('Documentation')
          .setURL('https://discord.js.org')
          .setStyle(ButtonStyle.Link)  // Link buttons don't emit events
      );

    // Select menu row (one per row, takes all 5 slots)
    const selectRow = new ActionRowBuilder()
      .addComponents(
        new StringSelectMenuBuilder()
          .setCustomId('select-role')
          .setPlaceholder('Select a role')
          .setMinValues(1)
          .setMaxValues(3)
          .addOptions([
            { label: 'Developer', value: 'dev', emoji: '💻' },
            { label: 'Designer', value: 'design', emoji: '🎨' },
            { label: 'Community', value: 'community', emoji: '🎉' }
          ])
      );

    await interaction.reply({
      content: 'Choose an option:',
      components: [buttonRow, selectRow]
    });

    // Collect responses
    const collector = interaction.channel.createMessageComponentCollector({
      filter: i => i.user.id === interaction.user.id,
      time: 60_000  // 60 seconds timeout
    });

    collector.on('collect', async i => {
      if (i.customId === 'confirm') {
        await i.update({ content: 'Confirmed!', components: [] });
        collector.stop();
      } else if (i.customId === 'cancel') {
        await i.update({ content: 'Cancelled', components: [] });
        collector.stop();
      } else if (i.customId === 'select-role') {
        await i.update({ content: `You selected: ${i.values.join(', ')}` });
      }
    });
  }
};
```

```javascript
// Modals (forms)
module.exports = {
  data: new SlashCommandBuilder()
    .setName('feedback')
    .setDescription('Submit feedback'),

  async execute(interaction) {
    const modal = new ModalBuilder()
      .setCustomId('feedback-modal')
      .setTitle('Submit Feedback');

    const titleInput = new TextInputBuilder()
      .setCustomId('feedback-title')
      .setLabel('Title')
      .setStyle(TextInputStyle.Short)
      .setRequired(true)
      .setMaxLength(100);

    const bodyInput = new TextInputBuilder()
      .setCustomId('feedback-body')
      .setLabel('Your feedback')
      .setStyle(TextInputStyle.Paragraph)
      .setRequired(true)
      .setMaxLength(1000)
      .setPlaceholder('Describe your feedback...');

    modal.addComponents(
      new ActionRowBuilder().addComponents(titleInput),
      new ActionRowBuilder().addComponents(bodyInput)
    );

    // Show modal - MUST be first response
    await interaction.showModal(modal);
  }
};

// Handle modal submission in interactionCreate
if (interaction.isModalSubmit()) {
  if (interaction.customId === 'feedback-modal') {
    const title = interaction.fields.getTextInputValue('feedback-title');
    const body = interaction.fields.getTextInputValue('feedback-body');

    await interaction.reply({
      content: `Thanks for your feedback!\n**${title}**\n${body}`,
      ephemeral: true
    });
  }
}
```

```python
# Pycord - Buttons and Views
import discord

class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button, interaction):
        self.value = True
        await interaction.response.edit_message(content="Confirmed!", view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button, interaction):
        self.value = False
        await interaction.response.edit_message(content="Cancelled", view=None)
        self.stop()

@bot.slash_command(name="confirm")
async def confirm_cmd(ctx: discord.ApplicationContext):
    view = ConfirmView()
    await ctx.respond("Are you sure?", view=view)

    await view.wait()  # Wait for user interaction
    if view.value is None:
        await ctx.followup.send("Timed out")

# Select Menu
class RoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Developer", value="dev", emoji="💻"),
            discord.SelectOption(label="Designer", value="design", emoji="🎨"),
        ]
        super().__init__(
            placeholder="Select roles...",
            min_values=1,
            max_values=2,
            options=options
        )

    async def callback(self, interaction):
        await interaction.response.send_message(
            f"You selected: {', '.join(self.values)}",
            ephemeral=True
        )

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RoleSelect())

# Modal
class FeedbackModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Submit Feedback")

        self.add_item(discord.ui.InputText(
            label="Title",
            style=discord.InputTextStyle.short,
            required=True,
            max_length=100
        ))
        self.add_item(discord.ui.InputText(
            label="Feedback",
            style=discord.InputTextStyle.long,
            required=True,
            max_length=1000
        ))

    async def callback(self, interaction):
        title = self.children[0].value
        body = self.children[1].value
        await interaction.response.send_message(
            f"Thanks!\n**{title}**\n{body}",
            ephemeral=True
        )

@bot.slash_command(name="feedback")
async def feedback(ctx: discord.ApplicationContext):
    await ctx.send_modal(FeedbackModal())
```

### 限制

- 每条消息/模态框最多 5 个 ActionRow
- 每个 ActionRow 最多 5 个按钮
- 每个 ActionRow 只能放 1 个选择菜单（占用全部 5 个槽位）
- 每条消息最多 5 个选择菜单
- 每个选择菜单最多 25 个选项
- 模态框必须是第一个响应（不能先 defer）

### 延迟响应模式

处理慢操作而不超时

**何时使用**: 操作耗时超过 3 秒、数据库查询、API 调用、LLM 响应、文件处理或生成

```javascript
// Discord.js - Deferred response
module.exports = {
  data: new SlashCommandBuilder()
    .setName('slow-task')
    .setDescription('Performs a slow operation'),

  async execute(interaction) {
    // Defer immediately - you have 3 seconds!
    await interaction.deferReply();
    // For ephemeral: await interaction.deferReply({ ephemeral: true });

    try {
      // Now you have 15 minutes to complete
      const result = await slowDatabaseQuery();
      const aiResponse = await callOpenAI(result);

      // Edit the deferred reply
      await interaction.editReply({
        content: `Result: ${aiResponse}`,
        embeds: [resultEmbed]
      });
    } catch (error) {
      await interaction.editReply({
        content: 'An error occurred while processing your request.'
      });
    }
  }
};

// For components (buttons, select menus)
collector.on('collect', async i => {
  await i.deferUpdate();  // Acknowledge without visual change
  // Or: await i.deferReply({ ephemeral: true });

  const result = await slowOperation();
  await i.editReply({ content: result });
});
```

```python
# Pycord - Deferred response
@bot.slash_command(name="slow-task")
async def slow_task(ctx: discord.ApplicationContext):
    # Defer immediately
    await ctx.defer()
    # For ephemeral: await ctx.defer(ephemeral=True)

    try:
        result = await slow_database_query()
        ai_response = await call_openai(result)

        await ctx.followup.send(f"Result: {ai_response}")
    except Exception as e:
        await ctx.followup.send("An error occurred")
```

### 时序

- 初始响应: 3 秒
- 延迟后续: 15 分钟
- 临时消息注意: 只能在初始响应时设置，之后无法更改

### Embed 构建器模式

专业外观的富嵌入消息

**何时使用**: 显示格式化信息、状态更新、帮助菜单、日志、结构化数据（字段、图片）

```javascript
const { EmbedBuilder, Colors } = require('discord.js');

// Basic embed
const embed = new EmbedBuilder()
  .setColor(Colors.Blue)
  .setTitle('Bot Status')
  .setURL('https://example.com')
  .setAuthor({
    name: 'Bot Name',
    iconURL: client.user.displayAvatarURL()
  })
  .setDescription('Current status and statistics')
  .addFields(
    { name: 'Servers', value: `${client.guilds.cache.size}`, inline: true },
    { name: 'Users', value: `${client.users.cache.size}`, inline: true },
    { name: 'Uptime', value: formatUptime(), inline: true }
  )
  .setThumbnail(client.user.displayAvatarURL())
  .setImage('https://example.com/banner.png')
  .setTimestamp()
  .setFooter({
    text: 'Requested by User',
    iconURL: interaction.user.displayAvatarURL()
  });

await interaction.reply({ embeds: [embed] });

// Multiple embeds (max 10)
await interaction.reply({ embeds: [embed1, embed2, embed3] });
```

```python
# Pycord
embed = discord.Embed(
    title="Bot Status",
    description="Current status and statistics",
    color=discord.Color.blue(),
    url="https://example.com"
)
embed.set_author(
    name="Bot Name",
    icon_url=bot.user.display_avatar.url
)
embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
embed.add_field(name="Users", value=len(bot.users), inline=True)
embed.set_thumbnail(url=bot.user.display_avatar.url)
embed.set_image(url="https://example.com/banner.png")
embed.set_footer(text="Requested by User", icon_url=ctx.author.display_avatar.url)
embed.timestamp = discord.utils.utcnow()

await ctx.respond(embed=embed)
```

### 限制

- 每条消息最多 10 个 embed
- 所有 embed 总共最多 6000 字符
- 标题最多 256 字符
- 描述最多 4096 字符
- 每个 embed 最多 25 个字段
- 字段名最多 256 字符
- 字段值最多 1024 字符

### 速率限制处理模式

优雅处理 Discord API 速率限制

**何时使用**: 高频操作、批量消息或角色分配、任何重复 API 调用

```javascript
// Discord.js handles rate limits automatically, but for custom handling:
const { REST } = require('discord.js');

const rest = new REST({ version: '10' })
  .setToken(process.env.DISCORD_TOKEN);

rest.on('rateLimited', (info) => {
  console.log(`Rate limited! Retry after ${info.retryAfter}ms`);
  console.log(`Route: ${info.route}`);
  console.log(`Global: ${info.global}`);
});

// Queue pattern for bulk operations
class RateLimitQueue {
  constructor() {
    this.queue = [];
    this.processing = false;
    this.requestsPerSecond = 40; // Safe margin below 50
  }

  async add(operation) {
    return new Promise((resolve, reject) => {
      this.queue.push({ operation, resolve, reject });
      this.process();
    });
  }

  async process() {
    if (this.processing || this.queue.length === 0) return;
    this.processing = true;

    while (this.queue.length > 0) {
      const { operation, resolve, reject } = this.queue.shift();

      try {
        const result = await operation();
        resolve(result);
      } catch (error) {
        reject(error);
      }

      // Throttle: ~40 requests per second
      await new Promise(r => setTimeout(r, 1000 / this.requestsPerSecond));
    }

    this.processing = false;
  }
}

const queue = new RateLimitQueue();

// Usage: Send 200 messages without hitting rate limits
for (const user of users) {
  await queue.add(() => user.send('Welcome!'));
}
```

```python
# Pycord/discord.py handles rate limits automatically
# For custom handling:
import asyncio
from collections import deque

class RateLimitQueue:
    def __init__(self, requests_per_second=40):
        self.queue = deque()
        self.processing = False
        self.delay = 1 / requests_per_second

    async def add(self, coro):
        future = asyncio.Future()
        self.queue.append((coro, future))
        if not self.processing:
            asyncio.create_task(self._process())
        return await future

    async def _process(self):
        self.processing = True
        while self.queue:
            coro, future = self.queue.popleft()
            try:
                result = await coro
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            await asyncio.sleep(self.delay)
        self.processing = False

queue = RateLimitQueue()

# Usage
for member in guild.members:
    await queue.add(member.send("Welcome!"))
```

### 速率限制

- 全局: 每秒 50 个请求
- Gateway: 每 60 秒 120 个请求
- 特定: 同一频道消息: 5条/5秒, 批量删除: 1次/秒, 公会成员请求: 因公会规模而异

### 分片模式

使用分片将机器人扩展到 2500+ 服务器

**何时使用**: 机器人接近 2500 个公会（必需）、需要水平扩展、大型机器人的内存优化

```javascript
// Discord.js Sharding Manager
// shard.js (main entry)
const { ShardingManager } = require('discord.js');

const manager = new ShardingManager('./bot.js', {
  token: process.env.DISCORD_TOKEN,
  totalShards: 'auto',  // Discord determines optimal count
  // Or specify: totalShards: 4
});

manager.on('shardCreate', shard => {
  console.log(`Launched shard ${shard.id}`);

  shard.on('ready', () => {
    console.log(`Shard ${shard.id} ready`);
  });

  shard.on('disconnect', () => {
    console.log(`Shard ${shard.id} disconnected`);
  });
});

manager.spawn();

// bot.js - Modified for sharding
const { Client } = require('discord.js');

const client = new Client({ intents: [...] });

// Get shard info
client.on('ready', () => {
  console.log(`Shard ${client.shard.ids[0]} ready with ${client.guilds.cache.size} guilds`);
});

// Cross-shard data
async function getTotalGuilds() {
  const results = await client.shard.fetchClientValues('guilds.cache.size');
  return results.reduce((acc, count) => acc + count, 0);
}

// Broadcast to all shards
async function broadcastMessage(channelId, message) {
  await client.shard.broadcastEval(
    (c, { channelId, message }) => {
      const channel = c.channels.cache.get(channelId);
      if (channel) channel.send(message);
    },
    { context: { channelId, message } }
  );
}
```

```python
# Pycord - AutoShardedBot
import discord
from discord.ext import commands

# Automatically handles sharding
bot = commands.AutoShardedBot(
    command_prefix="!",
    intents=discord.Intents.default(),
    shard_count=None  # Auto-determine
)

@bot.event
async def on_ready():
    print(f"Logged in on {len(bot.shards)} shards")
    for shard_id, shard in bot.shards.items():
        print(f"Shard {shard_id}: {shard.latency * 1000:.2f}ms")

@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} is ready")

# Get guilds per shard
for shard_id, guilds in bot.guilds_by_shard().items():
    print(f"Shard {shard_id}: {len(guilds)} guilds")
```

### 扩展指南

- 1-2500 个公会: 不需要分片
- 2500+ 个公会: Discord 要求分片
- 推荐: 每个分片约 1000 个公会
- 内存: 每个分片在独立进程中运行

## 陷阱

### 交互超时（3 秒规则）

严重程度: 关键

场景: 处理斜杠命令、按钮、选择菜单或模态框

症状:
用户看到 "This interaction failed" 或 "The application did not respond."
命令在本地正常但在生产环境失败。
慢操作永远无法完成。

原因:
Discord 要求所有交互在 3 秒内确认:
- 斜杠命令
- 按钮点击
- 选择菜单选择
- 右键菜单命令

如果在响应之前执行任何慢操作（数据库、API、文件 I/O），
就会错过时间窗口。即使机器人之后正确处理了请求，
Discord 也会显示错误。

确认后，你有 15 分钟时间进行后续响应。

推荐修复:

## 立即确认，稍后处理

```javascript
// Discord.js - Defer for slow operations
module.exports = {
  async execute(interaction) {
    // DEFER IMMEDIATELY - before any slow operation
    await interaction.deferReply();
    // For ephemeral: await interaction.deferReply({ ephemeral: true });

    // Now you have 15 minutes
    const result = await slowDatabaseQuery();
    const aiResponse = await callLLM(result);

    // Edit the deferred reply
    await interaction.editReply(`Result: ${aiResponse}`);
  }
};
```

```python
# Pycord
@bot.slash_command()
async def slow_command(ctx):
    await ctx.defer()  # Acknowledge immediately
    # await ctx.defer(ephemeral=True)  # For private response

    result = await slow_operation()
    await ctx.followup.send(f"Result: {result}")
```

## 对于组件（按钮、菜单）

```javascript
// If you're updating the message
await interaction.deferUpdate();

// If you're sending a new response
await interaction.deferReply({ ephemeral: true });
```

### 缺少特权 Intent 配置

严重程度: 关键

场景: 机器人需要成员数据、在线状态或消息内容

症状:
Members intent: 成员列表为空，on_member_join 不触发
Presences intent: 状态始终未知/离线
Message content intent: message.content 为空字符串

原因:
Discord 有 3 个特权 intents 需要手动启用:
1. **GUILD_MEMBERS** - 成员加入/离开、成员列表
2. **GUILD_PRESENCES** - 在线状态、活动
3. **MESSAGE_CONTENT** - 读取消息文本（用于命令已弃用）

这些必须:
1. 在 Discord Developer Portal > Bot > Privileged Gateway Intents 中启用
2. 在机器人代码中请求

在 100+ 服务器时，需要 Discord 验证才能继续使用它们。

推荐修复:

## 步骤 1: 在开发者门户启用

```
1. Go to https://discord.com/developers/applications
2. Select your application
3. Go to Bot section
4. Scroll to Privileged Gateway Intents
5. Toggle ON the intents you need
```

## 步骤 2: 在代码中请求

```javascript
// Discord.js
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,       // PRIVILEGED
    // GatewayIntentBits.GuildPresences,  // PRIVILEGED
    // GatewayIntentBits.MessageContent,  // PRIVILEGED - avoid!
  ]
});
```

```python
# Pycord
intents = discord.Intents.default()
intents.members = True       # PRIVILEGED
# intents.presences = True   # PRIVILEGED
# intents.message_content = True  # PRIVILEGED - avoid!

bot = commands.Bot(intents=intents)
```

## 尽可能避免 Message Content Intent

使用斜杠命令、按钮和模态框代替消息解析。
这些不需要 Message Content intent。

### 命令注册被限速

严重程度: 高

场景: 注册斜杠命令

症状:
命令未出现。部署时出现 429 错误。
"You are being rate limited" 消息。
命令在某些公会出现但在其他公会没有。

原因:
命令注册有速率限制:
- 全局命令: 每天 200 次创建，更新最多需要 1 小时传播
- 公会命令: 每个公会每天 200 次创建，即时更新

常见错误:
- 每次机器人启动时注册命令
- 在每个公会单独注册
- 在循环中进行更改而没有延迟

推荐修复:

## 使用单独的部署脚本（不在启动时）

```javascript
// deploy-commands.js - Run manually, not on bot start
const { REST, Routes } = require('discord.js');

const rest = new REST().setToken(process.env.DISCORD_TOKEN);

async function deploy() {
  // For development: Guild commands (instant)
  if (process.env.GUILD_ID) {
    await rest.put(
      Routes.applicationGuildCommands(
        process.env.CLIENT_ID,
        process.env.GUILD_ID
      ),
      { body: commands }
    );
    console.log('Guild commands deployed instantly');
  }

  // For production: Global commands (up to 1 hour)
  else {
    await rest.put(
      Routes.applicationCommands(process.env.CLIENT_ID),
      { body: commands }
    );
    console.log('Global commands deployed (may take up to 1 hour)');
  }
}

deploy();
```

```python
# Pycord - Don't sync on every startup
@bot.event
async def on_ready():
    # DON'T DO THIS:
    # await bot.sync_commands()

    print(f"Ready! Commands should already be registered.")

# Instead, sync manually or use a flag
if __name__ == "__main__":
    if "--sync" in sys.argv:
        # Only sync when explicitly requested
        bot.sync_commands_on_start = True
    bot.run(token)
```

## 测试工作流

1. 开发期间使用公会命令（即时更新）
2. 准备好生产时才部署全局命令
3. 手动运行部署脚本，不要每次重启都运行

### Bot Token 泄露

严重程度: 关键

场景: 存储或分享机器人 token

症状:
机器人执行未授权操作。
机器人加入随机服务器。
机器人发送垃圾邮件或恶意内容。
Discord 使其失效后显示 "Invalid token"。

原因:
你的机器人 token 提供对机器人的完全控制。攻击者可以:
- 以你的机器人身份发送消息
- 加入服务器、创建邀请
- 访问你的机器人可以访问的所有数据
- 可能接管机器人有管理员权限的服务器

Discord 主动扫描 GitHub 查找泄露的 token 并使其失效。
常见泄露点:
- 提交到 Git
- 在 Discord 本身分享
- 在客户端代码中
- 在公开截图中

推荐修复:

## 永远不要硬编码 token

```javascript
// BAD - never do this
const token = 'MTIzNDU2Nzg5MDEyMzQ1Njc4.ABCDEF.xyz...';

// GOOD - environment variables
require('dotenv').config();
client.login(process.env.DISCORD_TOKEN);
```

## 使用 .gitignore

```
# .gitignore
.env
.env.local
config.json
```

## 如果 token 泄露

1. 立即前往 Developer Portal
2. 重新生成 token
3. 更新所有部署
4. 检查机器人活动是否有未授权操作
5. 检查 git 历史并在需要时强制推送删除

## 正确使用环境变量

```bash
# .env (never commit)
DISCORD_TOKEN=your_token_here
CLIENT_ID=your_client_id
```

```javascript
// Load with dotenv
require('dotenv').config();
const token = process.env.DISCORD_TOKEN;
```

### Bot 缺少 applications.commands Scope

严重程度: 高

场景: 斜杠命令对用户不显示

症状:
机器人在服务器中但斜杠命令不显示。
输入 / 没有显示你的机器人的命令。
命令在开发服务器正常但在其他服务器不行。

原因:
Discord 有两个重要的 OAuth scope:
- `bot` - 传统机器人权限（消息、反应等）
- `applications.commands` - 斜杠命令权限

许多机器人在斜杠命令存在之前仅使用 `bot` scope 邀请。
它们需要使用两个 scope 重新邀请。

推荐修复:

## 生成正确的邀请 URL

```
https://discord.com/api/oauth2/authorize
  ?client_id=YOUR_CLIENT_ID
  &permissions=0
  &scope=bot%20applications.commands
```

## 在 Discord Developer Portal 中

1. 前往 OAuth2 > URL Generator
2. 同时选择:
   - `bot`
   - `applications.commands`
3. 选择所需的机器人权限
4. 使用生成的 URL

## 无需踢出重新邀请

用户可以使用新的邀请 URL，即使机器人已在服务器中。
这会添加新的 scope 而不会移除机器人。

```javascript
// Generate invite URL in code
const inviteUrl = client.generateInvite({
  scopes: ['bot', 'applications.commands'],
  permissions: [
    'SendMessages',
    'EmbedLinks',
    // Add other needed permissions
  ]
});
```

### 全局命令未立即出现

严重程度: 中

场景: 部署全局斜杠命令

症状:
部署后命令不出现。
公会命令正常但全局命令不行。
一小时后命令出现。

原因:
全局命令可能需要长达 1 小时才能传播到所有 Discord 服务器。
这是 Discord 缓存和 CDN 的设计特性。

公会命令是即时的但只在特定公会工作。

推荐修复:

## 开发: 使用公会命令

```javascript
// Instant updates for testing
await rest.put(
  Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
  { body: commands }
);
```

## 生产: 在非高峰期部署全局命令

```javascript
// Takes up to 1 hour to propagate
await rest.put(
  Routes.applicationCommands(CLIENT_ID),
  { body: commands }
);
```

## 工作流

1. 使用公会命令开发和测试（即时）
2. 准备好后，部署全局命令
3. 等待最多 1 小时传播
4. 不要频繁部署全局命令

### 频繁的 Gateway 断开连接

严重程度: 中

场景: 机器人随机离线或错过事件

症状:
机器人间歇性显示离线。
事件被错过（成员加入、消息）。
日志中有重连消息。

原因:
Discord gateway 需要定期心跳。问题:
- 阻塞操作阻止心跳
- 网络不稳定
- 内存压力导致 GC 暂停
- 太多公会而没有分片（2500+ 需要分片）

推荐修复:

## 永远不要阻塞事件循环

```javascript
// BAD - blocks event loop
const data = fs.readFileSync('file.json');

// GOOD - async
const data = await fs.promises.readFile('file.json');
```

## 优雅处理重连

```javascript
client.on('shardResume', (id, replayedEvents) => {
  console.log(`Shard ${id} resumed, replayed ${replayedEvents} events`);
});

client.on('shardDisconnect', (event, id) => {
  console.log(`Shard ${id} disconnected`);
});

client.on('shardReconnecting', (id) => {
  console.log(`Shard ${id} reconnecting...`);
});
```

## 大规模实现分片

```javascript
// Required at 2500+ guilds
const manager = new ShardingManager('./bot.js', {
  token: process.env.DISCORD_TOKEN,
  totalShards: 'auto'
});
manager.spawn();
```

### 模态框必须是第一个响应

严重程度: 中

场景: 从斜杠命令或按钮显示模态框

症状:
"Interaction has already been acknowledged" 错误。
模态框不出现。
有时有效有时无效。

原因:
模态框有一个特殊要求: 显示模态框必须是对交互的第一个响应。你不能:
- defer() 然后 showModal()
- reply() 然后 showModal()
- 思考超过 3 秒然后 showModal()

推荐修复:

## 立即显示模态框

```javascript
// CORRECT - modal is first response
async execute(interaction) {
  const modal = new ModalBuilder()
    .setCustomId('my-modal')
    .setTitle('Input Form');

  // Show immediately - no defer, no reply first
  await interaction.showModal(modal);
}
```

```javascript
// WRONG - deferred first
async execute(interaction) {
  await interaction.deferReply();  // CAN'T DO THIS
  await interaction.showModal(modal);  // Will fail
}
```

## 如果需要先检查某些内容

```javascript
async execute(interaction) {
  // Quick sync check is OK (under 3 seconds)
  if (!hasPermission(interaction.user.id)) {
    return interaction.reply({
      content: 'No permission',
      ephemeral: true
    });
  }

  // Show modal (still first interaction response for this path)
  await interaction.showModal(modal);
}
```

## 验证检查

### 硬编码 Discord Token

严重程度: 错误

Discord token 永远不应该硬编码

消息: 检测到硬编码的 Discord token。请使用环境变量。

### Token 变量赋值

严重程度: 错误

Token 应该来自环境变量，而非字符串

消息: Token 从字符串字面量赋值。请使用环境变量。

### 客户端代码中的 Token

严重程度: 错误

永远不要向浏览器暴露 Discord token

消息: Discord 凭证暴露在客户端。只能在服务器端使用。

### 慢操作没有 Defer

严重程度: 警告

慢操作应该延迟以避免超时

消息: 慢操作没有 defer。交互可能超时。

### 交互没有错误处理

严重程度: 警告

交互应该有 try/catch 进行优雅的错误处理

消息: 交互没有错误处理。请添加 try/catch。

### 使用 Message Content Intent

严重程度: 警告

Message Content 是特权 intent，优先使用斜杠命令

消息: 使用了 Message Content intent。请考虑改用斜杠命令。

### 请求所有 Intents

严重程度: 警告

只请求你实际需要的 intents

消息: 请求了所有 intents。只启用你需要的。

### 在 Ready 事件中同步命令

严重程度: 警告

不要在每次机器人启动时同步命令

消息: 在启动时同步命令。请使用单独的部署脚本。

### 在循环中注册命令

严重程度: 警告

使用批量注册，而非单独调用

消息: 在循环中注册命令。请使用批量注册。

### 没有速率限制处理

严重程度: 信息

考虑为批量操作处理速率限制

消息: 批量操作没有速率限制处理。

## 协作

### 委托触发

- 用户需要 AI 驱动的 Discord 机器人 -> llm-architect (集成 LLM 实现对话式 Discord 机器人)
- 用户也需要 Slack 集成 -> slack-bot-builder (跨平台机器人架构)
- 用户需要语音功能 -> voice-agents (Discord 语音频道集成)
- 用户需要机器人数据的数据库 -> postgres-wizard (存储用户数据、服务器配置、审核日志)
- 用户需要工作流自动化 -> workflow-automation (Discord 事件触发工作流)
- 用户需要高可用性 -> devops (分片、扩展、监控大型机器人)
- 用户需要支付集成 -> stripe-specialist (高级机器人功能、订阅管理)

## 何时使用
当请求明显匹配上述能力和模式时使用此技能。

## 限制
- 仅当任务明显匹配上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
