# Solidity 安全实现手册

本文件包含该技能引用的详细模式、清单和代码示例。

# Solidity 安全

掌握智能合约安全最佳实践、漏洞预防和安全的 Solidity 开发模式。

## 何时使用此技能

- 编写安全的智能合约
- 审计现有合约的漏洞
- 实现安全的 DeFi 协议
- 防止重入攻击、溢出和访问控制问题
- 在保持安全性的同时优化 gas 用量
- 为专业审计准备合约
- 了解常见攻击向量

## 关键漏洞

### 1. 重入攻击

攻击者在状态更新之前回调你的合约。

**存在漏洞的代码：**

```solidity
// VULNERABLE TO REENTRANCY
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];

        // DANGER: External call before state update
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);

        balances[msg.sender] = 0;  // Too late!
    }
}
```

**安全模式（检查-效果-交互）：**

```solidity
contract SecureBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        // EFFECTS: Update state BEFORE external call
        balances[msg.sender] = 0;

        // INTERACTIONS: External call last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

**替代方案：ReentrancyGuard**

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 2. 整数溢出/下溢

**存在漏洞的代码（Solidity < 0.8.0）：**

```solidity
// VULNERABLE
contract VulnerableToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // No overflow check - can wrap around
        balances[msg.sender] -= amount;  // Can underflow!
        balances[to] += amount;          // Can overflow!
    }
}
```

**安全模式（Solidity >= 0.8.0）：**

```solidity
// Solidity 0.8+ has built-in overflow/underflow checks
contract SecureToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // Automatically reverts on overflow/underflow
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

**对于 Solidity < 0.8.0，使用 SafeMath：**

```solidity
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SecureToken {
    using SafeMath for uint256;
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[to] = balances[to].add(amount);
    }
}
```

### 3. 访问控制

**存在漏洞的代码：**

```solidity
// VULNERABLE: Anyone can call critical functions
contract VulnerableContract {
    address public owner;

    function withdraw(uint256 amount) public {
        // No access control!
        payable(msg.sender).transfer(amount);
    }
}
```

**安全模式：**

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is Ownable {
    function withdraw(uint256 amount) public onlyOwner {
        payable(owner()).transfer(amount);
    }
}

// Or implement custom role-based access
contract RoleBasedContract {
    mapping(address => bool) public admins;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Not an admin");
        _;
    }

    function criticalFunction() public onlyAdmin {
        // Protected function
    }
}
```

### 4. 抢跑交易

**存在漏洞：**

```solidity
// VULNERABLE TO FRONT-RUNNING
contract VulnerableDEX {
    function swap(uint256 amount, uint256 minOutput) public {
        // Attacker sees this in mempool and front-runs
        uint256 output = calculateOutput(amount);
        require(output >= minOutput, "Slippage too high");
        // Perform swap
    }
}
```

**缓解措施：**

```solidity
contract SecureDEX {
    mapping(bytes32 => bool) public usedCommitments;

    // Step 1: Commit to trade
    function commitTrade(bytes32 commitment) public {
        usedCommitments[commitment] = true;
    }

    // Step 2: Reveal trade (next block)
    function revealTrade(
        uint256 amount,
        uint256 minOutput,
        bytes32 secret
    ) public {
        bytes32 commitment = keccak256(abi.encodePacked(
            msg.sender, amount, minOutput, secret
        ));
        require(usedCommitments[commitment], "Invalid commitment");
        // Perform swap
    }
}
```

## 安全最佳实践

### 检查-效果-交互模式

```solidity
contract SecurePattern {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) public {
        // 1. CHECKS: Validate conditions
        require(amount <= balances[msg.sender], "Insufficient balance");
        require(amount > 0, "Amount must be positive");

        // 2. EFFECTS: Update state
        balances[msg.sender] -= amount;

        // 3. INTERACTIONS: External calls last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 拉取优于推送模式

```solidity
// Prefer this (pull)
contract SecurePayment {
    mapping(address => uint256) public pendingWithdrawals;

    function recordPayment(address recipient, uint256 amount) internal {
        pendingWithdrawals[recipient] += amount;
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to withdraw");

        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}

// Over this (push)
contract RiskyPayment {
    function distributePayments(address[] memory recipients, uint256[] memory amounts) public {
        for (uint i = 0; i < recipients.length; i++) {
            // If any transfer fails, entire batch fails
            payable(recipients[i]).transfer(amounts[i]);
        }
    }
}
```

### 输入验证

```solidity
contract SecureContract {
    function transfer(address to, uint256 amount) public {
        // Validate inputs
        require(to != address(0), "Invalid recipient");
        require(to != address(this), "Cannot send to contract");
        require(amount > 0, "Amount must be positive");
        require(amount <= balances[msg.sender], "Insufficient balance");

        // Proceed with transfer
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### 紧急停止（断路器）

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyStop is Pausable, Ownable {
    function criticalFunction() public whenNotPaused {
        // Function logic
    }

    function emergencyStop() public onlyOwner {
        _pause();
    }

    function resume() public onlyOwner {
        _unpause();
    }
}
```

## Gas 优化

### 使用 `uint256` 而非更小的类型

```solidity
// More gas efficient
contract GasEfficient {
    uint256 public value;  // Optimal

    function set(uint256 _value) public {
        value = _value;
    }
}

// Less efficient
contract GasInefficient {
    uint8 public value;  // Still uses 256-bit slot

    function set(uint8 _value) public {
        value = _value;  // Extra gas for type conversion
    }
}
```

### 打包存储变量

```solidity
// Gas efficient (3 variables in 1 slot)
contract PackedStorage {
    uint128 public a;  // Slot 0
    uint64 public b;   // Slot 0
    uint64 public c;   // Slot 0
    uint256 public d;  // Slot 1
}

// Gas inefficient (each variable in separate slot)
contract UnpackedStorage {
    uint256 public a;  // Slot 0
    uint256 public b;  // Slot 1
    uint256 public c;  // Slot 2
    uint256 public d;  // Slot 3
}
```

### 函数参数使用 `calldata` 而非 `memory`

```solidity
contract GasOptimized {
    // More gas efficient
    function processData(uint256[] calldata data) public pure returns (uint256) {
        return data[0];
    }

    // Less efficient
    function processDataMemory(uint256[] memory data) public pure returns (uint256) {
        return data[0];
    }
}
```

### 适当使用事件存储数据

```solidity
contract EventStorage {
    // Emitting events is cheaper than storage
    event DataStored(address indexed user, uint256 indexed id, bytes data);

    function storeData(uint256 id, bytes calldata data) public {
        emit DataStored(msg.sender, id, data);
        // Don't store in contract storage unless needed
    }
}
```

## 常见漏洞清单

```solidity
// Security Checklist Contract
contract SecurityChecklist {
    /**
     * [ ] Reentrancy protection (ReentrancyGuard or CEI pattern)
     * [ ] Integer overflow/underflow (Solidity 0.8+ or SafeMath)
     * [ ] Access control (Ownable, roles, modifiers)
     * [ ] Input validation (require statements)
     * [ ] Front-running mitigation (commit-reveal if applicable)
     * [ ] Gas optimization (packed storage, calldata)
     * [ ] Emergency stop mechanism (Pausable)
     * [ ] Pull over push pattern for payments
     * [ ] No delegatecall to untrusted contracts
     * [ ] No tx.origin for authentication (use msg.sender)
     * [ ] Proper event emission
     * [ ] External calls at end of function
     * [ ] Check return values of external calls
     * [ ] No hardcoded addresses
     * [ ] Upgrade mechanism (if proxy pattern)
     */
}
```

## 安全测试

```javascript
// Hardhat test example
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function () {
  it("Should prevent reentrancy attack", async function () {
    const [attacker] = await ethers.getSigners();

    const VictimBank = await ethers.getContractFactory("SecureBank");
    const bank = await VictimBank.deploy();

    const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
    const attackerContract = await Attacker.deploy(bank.address);

    // Deposit funds
    await bank.deposit({ value: ethers.utils.parseEther("10") });

    // Attempt reentrancy attack
    await expect(
      attackerContract.attack({ value: ethers.utils.parseEther("1") }),
    ).to.be.revertedWith("ReentrancyGuard: reentrant call");
  });

  it("Should prevent integer overflow", async function () {
    const Token = await ethers.getContractFactory("SecureToken");
    const token = await Token.deploy();

    // Attempt overflow
    await expect(token.transfer(attacker.address, ethers.constants.MaxUint256))
      .to.be.reverted;
  });

  it("Should enforce access control", async function () {
    const [owner, attacker] = await ethers.getSigners();

    const Contract = await ethers.getContractFactory("SecureContract");
    const contract = await Contract.deploy();

    // Attempt unauthorized withdrawal
    await expect(contract.connect(attacker).withdraw(100)).to.be.revertedWith(
      "Ownable: caller is not the owner",
    );
  });
});
```

## 审计准备

```solidity
contract WellDocumentedContract {
    /**
     * @title Well Documented Contract
     * @dev Example of proper documentation for audits
     * @notice This contract handles user deposits and withdrawals
     */

    /// @notice Mapping of user balances
    mapping(address => uint256) public balances;

    /**
     * @dev Deposits ETH into the contract
     * @notice Anyone can deposit funds
     */
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    /**
     * @dev Withdraws user's balance
     * @notice Follows CEI pattern to prevent reentrancy
     * @param amount Amount to withdraw in wei
     */
    function withdraw(uint256 amount) public {
        // CHECKS
        require(amount <= balances[msg.sender], "Insufficient balance");

        // EFFECTS
        balances[msg.sender] -= amount;

        // INTERACTIONS
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## 参考资料

- **references/reentrancy.md**：全面的重入攻击防护
- **references/access-control.md**：基于角色的访问模式
- **references/overflow-underflow.md**：SafeMath 和整数安全
- **references/gas-optimization.md**：Gas 节省技巧
- **references/vulnerability-patterns.md**：常见漏洞目录
- **assets/solidity-contracts-templates.sol**：安全合约模板
- **assets/security-checklist.md**：审计前清单
- **scripts/analyze-contract.sh**：静态分析工具

## 安全分析工具

- **Slither**：静态分析工具
- **Mythril**：安全分析工具
- **Echidna**：模糊测试工具
- **Manticore**：符号执行
- **Securify**：自动化安全扫描器

## 常见陷阱

1. **使用 `tx.origin` 进行身份验证**：应改用 `msg.sender`
2. **未检查的外部调用**：始终检查返回值
3. **对不受信任的合约使用 Delegatecall**：可能劫持你的合约
4. **浮动 Pragma**：固定到特定的 Solidity 版本
5. **缺少事件**：对状态变更发出事件
6. **循环中消耗过多 Gas**：可能触及区块 gas 上限
7. **没有升级路径**：如果需要升级，考虑代理模式
