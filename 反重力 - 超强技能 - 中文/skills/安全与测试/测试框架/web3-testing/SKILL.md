---
name: web3-testing
description: "掌握使用 Hardhat、Foundry 及高级测试模式进行智能合约测试的全面策略。触发词：web3测试、smart contract testing、智能合约测试、Hardhat测试、Foundry测试、gas优化、模糊测试、主网分叉"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Web3 智能合约测试

掌握使用 Hardhat、Foundry 及高级测试模式进行智能合约测试的全面策略。

## 不要在以下场景使用此技能

- 任务与 web3 智能合约测试无关
- 需要本范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如果需要详细的示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的场景

- 为智能合约编写单元测试
- 搭建集成测试套件
- 执行 gas 优化测试
- 对边界情况进行模糊测试
- 分叉主网以进行真实环境测试
- 自动化测试覆盖率报告
- 在 Etherscan 上验证合约

## Hardhat 测试配置

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("@nomiclabs/hardhat-etherscan");
require("hardhat-gas-reporter");
require("solidity-coverage");

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      forking: {
        url: process.env.MAINNET_RPC_URL,
        blockNumber: 15000000,
      },
    },
    goerli: {
      url: process.env.GOERLI_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
  gasReporter: {
    enabled: true,
    currency: "USD",
    coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
};
```

## 单元测试模式

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");
const {
  loadFixture,
  time,
} = require("@nomicfoundation/hardhat-network-helpers");

describe("Token Contract", function () {
  // Fixture for test setup
  async function deployTokenFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy();

    return { token, owner, addr1, addr2 };
  }

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      const { token, owner } = await loadFixture(deployTokenFixture);
      expect(await token.owner()).to.equal(owner.address);
    });

    it("Should assign total supply to owner", async function () {
      const { token, owner } = await loadFixture(deployTokenFixture);
      const ownerBalance = await token.balanceOf(owner.address);
      expect(await token.totalSupply()).to.equal(ownerBalance);
    });
  });

  describe("Transactions", function () {
    it("Should transfer tokens between accounts", async function () {
      const { token, owner, addr1 } = await loadFixture(deployTokenFixture);

      await expect(token.transfer(addr1.address, 50)).to.changeTokenBalances(
        token,
        [owner, addr1],
        [-50, 50],
      );
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      const { token, addr1 } = await loadFixture(deployTokenFixture);
      const initialBalance = await token.balanceOf(addr1.address);

      await expect(
        token.connect(addr1).transfer(owner.address, 1),
      ).to.be.revertedWith("Insufficient balance");
    });

    it("Should emit Transfer event", async function () {
      const { token, owner, addr1 } = await loadFixture(deployTokenFixture);

      await expect(token.transfer(addr1.address, 50))
        .to.emit(token, "Transfer")
        .withArgs(owner.address, addr1.address, 50);
    });
  });

  describe("Time-based tests", function () {
    it("Should handle time-locked operations", async function () {
      const { token } = await loadFixture(deployTokenFixture);

      // Increase time by 1 day
      await time.increase(86400);

      // Test time-dependent functionality
    });
  });

  describe("Gas optimization", function () {
    it("Should use gas efficiently", async function () {
      const { token } = await loadFixture(deployTokenFixture);

      const tx = await token.transfer(addr1.address, 100);
      const receipt = await tx.wait();

      expect(receipt.gasUsed).to.be.lessThan(50000);
    });
  });
});
```

## Foundry 测试（Forge）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/Token.sol";

contract TokenTest is Test {
    Token token;
    address owner = address(1);
    address user1 = address(2);
    address user2 = address(3);

    function setUp() public {
        vm.prank(owner);
        token = new Token();
    }

    function testInitialSupply() public {
        assertEq(token.totalSupply(), 1000000 * 10**18);
    }

    function testTransfer() public {
        vm.prank(owner);
        token.transfer(user1, 100);

        assertEq(token.balanceOf(user1), 100);
        assertEq(token.balanceOf(owner), token.totalSupply() - 100);
    }

    function testFailTransferInsufficientBalance() public {
        vm.prank(user1);
        token.transfer(user2, 100); // Should fail
    }

    function testCannotTransferToZeroAddress() public {
        vm.prank(owner);
        vm.expectRevert("Invalid recipient");
        token.transfer(address(0), 100);
    }

    // Fuzzing test
    function testFuzzTransfer(uint256 amount) public {
        vm.assume(amount > 0 && amount <= token.totalSupply());

        vm.prank(owner);
        token.transfer(user1, amount);

        assertEq(token.balanceOf(user1), amount);
    }

    // Test with cheatcodes
    function testDealAndPrank() public {
        // Give ETH to address
        vm.deal(user1, 10 ether);

        // Impersonate address
        vm.prank(user1);

        // Test functionality
        assertEq(user1.balance, 10 ether);
    }

    // Mainnet fork test
    function testForkMainnet() public {
        vm.createSelectFork("https://eth-mainnet.alchemyapi.io/v2/...");

        // Interact with mainnet contracts
        address dai = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
        assertEq(IERC20(dai).symbol(), "DAI");
    }
}
```

## 高级测试模式

### 快照与回滚

```javascript
describe("Complex State Changes", function () {
  let snapshotId;

  beforeEach(async function () {
    snapshotId = await network.provider.send("evm_snapshot");
  });

  afterEach(async function () {
    await network.provider.send("evm_revert", [snapshotId]);
  });

  it("Test 1", async function () {
    // Make state changes
  });

  it("Test 2", async function () {
    // State reverted, clean slate
  });
});
```

### 主网分叉

```javascript
describe("Mainnet Fork Tests", function () {
  let uniswapRouter, dai, usdc;

  before(async function () {
    await network.provider.request({
      method: "hardhat_reset",
      params: [
        {
          forking: {
            jsonRpcUrl: process.env.MAINNET_RPC_URL,
            blockNumber: 15000000,
          },
        },
      ],
    });

    // Connect to existing mainnet contracts
    uniswapRouter = await ethers.getContractAt(
      "IUniswapV2Router",
      "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    );

    dai = await ethers.getContractAt(
      "IERC20",
      "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    );
  });

  it("Should swap on Uniswap", async function () {
    // Test with real Uniswap contracts
  });
});
```

### 模拟账户

```javascript
it("Should impersonate whale account", async function () {
  const whaleAddress = "0x...";

  await network.provider.request({
    method: "hardhat_impersonateAccount",
    params: [whaleAddress],
  });

  const whale = await ethers.getSigner(whaleAddress);

  // Use whale's tokens
  await dai
    .connect(whale)
    .transfer(addr1.address, ethers.utils.parseEther("1000"));
});
```

## Gas 优化测试

```javascript
const { expect } = require("chai");

describe("Gas Optimization", function () {
  it("Compare gas usage between implementations", async function () {
    const Implementation1 =
      await ethers.getContractFactory("OptimizedContract");
    const Implementation2 = await ethers.getContractFactory(
      "UnoptimizedContract",
    );

    const contract1 = await Implementation1.deploy();
    const contract2 = await Implementation2.deploy();

    const tx1 = await contract1.doSomething();
    const receipt1 = await tx1.wait();

    const tx2 = await contract2.doSomething();
    const receipt2 = await tx2.wait();

    console.log("Optimized gas:", receipt1.gasUsed.toString());
    console.log("Unoptimized gas:", receipt2.gasUsed.toString());

    expect(receipt1.gasUsed).to.be.lessThan(receipt2.gasUsed);
  });
});
```

## 覆盖率报告

```bash
# Generate coverage report
npx hardhat coverage

# Output shows:
# File                | % Stmts | % Branch | % Funcs | % Lines |
# -------------------|---------|----------|---------|---------|
# contracts/Token.sol |   100   |   90     |   100   |   95    |
```

## 合约验证

```javascript
// Verify on Etherscan
await hre.run("verify:verify", {
  address: contractAddress,
  constructorArguments: [arg1, arg2],
});
```

```bash
# Or via CLI
npx hardhat verify --network mainnet CONTRACT_ADDRESS "Constructor arg1" "arg2"
```

## CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: "16"

      - run: npm install
      - run: npx hardhat compile
      - run: npx hardhat test
      - run: npx hardhat coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
```

## 资源

- **references/hardhat-setup.md**：Hardhat 配置指南
- **references/foundry-setup.md**：Foundry 测试框架
- **references/test-patterns.md**：测试最佳实践
- **references/mainnet-forking.md**：分叉测试策略
- **references/contract-verification.md**：Etherscan 验证
- **assets/hardhat-config.js**：完整 Hardhat 配置
- **assets/test-suite.js**：综合测试示例
- **assets/foundry.toml**：Foundry 配置
- **scripts/test-contract.sh**：自动化测试脚本

## 最佳实践

1. **测试覆盖率**：力争 >90% 的覆盖率
2. **边界条件**：测试临界值情况
3. **Gas 上限**：验证函数不会触及区块 gas 上限
4. **重入攻击**：测试是否存在重入漏洞
5. **访问控制**：测试未授权的访问尝试
6. **事件**：验证事件是否正确触发
7. **测试装置**：使用 fixtures 避免代码重复
8. **主网分叉**：使用真实合约进行测试
9. **模糊测试**：使用基于属性的测试
10. **CI/CD**：在每次提交时自动运行测试

## 限制说明
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出结果视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来并请求澄清。
