---
name: firebase
description: Firebase 让你在几分钟内拥有完整的后端——认证、数据库、存储、函数、托管。但便捷的设置背后隐藏着真正的复杂性。安全规则是你的最后一道防线，而它们经常出错。触发词：Firebase、Firestore、Firebase Auth、Cloud Functions、Firebase Storage、Realtime Database、Firebase Hosting、Firebase Emulator、Security Rules、Firebase Admin、firebase、firestore、firebase auth、cloud functions
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Firebase

Firebase 让你在几分钟内拥有完整的后端——认证、数据库、存储、函数、托管。但便捷的设置背后隐藏着真正的复杂性。安全规则是你的最后一道防线，而它们经常出错。Firestore 查询能力有限，而这通常是在你设计完数据模型之后才发现的。

本技能涵盖 Firebase Authentication、Firestore、Realtime Database、Cloud Functions、Cloud Storage 和 Firebase Hosting。核心洞察：Firebase 为读取密集型、反规范化数据进行了优化。如果你还在用关系型思维思考，那你的思路就错了。

2025 年的教训：Firestore 的定价可能会让你大吃一惊。读取操作起初很便宜，但很快就会变得昂贵。一个设计不当的监听器可能比专用数据库成本更高。根据查询模式而非数据关系来规划数据模型。

## 原则

- 为查询设计数据，而非关系
- 安全规则是必须的，不是可选的
- 积极反规范化——重复成本低，连接成本高
- 使用批量写入和事务保证一致性
- 明智使用离线持久化——它不是免费的
- 用 Cloud Functions 处理客户端不该做的事情
- 基于环境的配置，永远不要在客户端硬编码密钥

## 能力

- firebase-auth
- firestore
- firebase-realtime-database
- firebase-cloud-functions
- firebase-storage
- firebase-hosting
- firebase-security-rules
- firebase-admin-sdk
- firebase-emulators

## 范围

- general-backend-architecture -> backend
- payment-processing -> stripe
- email-sending -> email
- advanced-auth-flows -> authentication-oauth
- kubernetes-deployment -> devops

## 工具

### 核心

- firebase - 使用场景：客户端 SDK 注意：模块化 SDK - 支持摇树优化
- firebase-admin - 使用场景：服务端 / Cloud Functions 注意：完全访问权限，绕过安全规则
- firebase-functions - 使用场景：Cloud Functions v2 注意：推荐使用 v2 函数

### 测试

- @firebase/rules-unit-testing - 使用场景：测试安全规则 注意：必不可少——规则 bug 就是安全 bug
- firebase-tools - 使用场景：模拟器套件 注意：本地开发无需访问生产环境

### 框架

- reactfire - 使用场景：React + Firebase 注意：基于 Hooks，处理订阅
- vuefire - 使用场景：Vue + Firebase 注意：Vue 专用绑定
- angularfire - 使用场景：Angular + Firebase 注意：官方 Angular 绑定

## 模式

### 模块化 SDK 导入

只导入你需要的内容以获得更小的打包体积

**何时使用**：客户端 Firebase 使用

# MODULAR IMPORTS:

"""
Firebase v9+ 使用模块化 SDK。只导入你需要的内容。
这支持摇树优化和更小的打包体积。
"""

// WRONG: v8-compat style (larger bundle)
import firebase from 'firebase/compat/app';
import 'firebase/compat/firestore';
const db = firebase.firestore();

// RIGHT: v9+ modular (tree-shakeable)
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, doc, getDoc } from 'firebase/firestore';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Get a document
const docRef = doc(db, 'users', 'userId');
const docSnap = await getDoc(docRef);

if (docSnap.exists()) {
  console.log(docSnap.data());
}

// Query with constraints
import { query, where, orderBy, limit } from 'firebase/firestore';

const q = query(
  collection(db, 'posts'),
  where('published', '==', true),
  orderBy('createdAt', 'desc'),
  limit(10)
);

### 安全规则设计

从第一天起就用正确的规则保护你的数据

**何时使用**：任何 Firestore 数据库

# FIRESTORE SECURITY RULES:

"""
规则是你的最后一道防线。每次读写都要经过它们。
如果写错了，你的数据就会暴露。
"""

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper functions
    function isSignedIn() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return request.auth.uid == userId;
    }

    function isAdmin() {
      return request.auth.token.admin == true;
    }

    // Users collection
    match /users/{userId} {
      // Anyone can read public profile
      allow read: if true;

      // Only owner can write their own data
      allow write: if isOwner(userId);

      // Private subcollection
      match /private/{document=**} {
        allow read, write: if isOwner(userId);
      }
    }

    // Posts collection
    match /posts/{postId} {
      // Anyone can read published posts
      allow read: if resource.data.published == true
                  || isOwner(resource.data.authorId);

      // Only authenticated users can create
      allow create: if isSignedIn()
                    && request.resource.data.authorId == request.auth.uid;

      // Only author can update/delete
      allow update, delete: if isOwner(resource.data.authorId);
    }

    // Admin-only collection
    match /admin/{document=**} {
      allow read, write: if isAdmin();
    }
  }
}

### 面向查询的数据建模

围绕查询模式设计 Firestore 数据结构

**何时使用**：设计 Firestore schema

# FIRESTORE DATA MODELING:

"""
Firestore 不是关系型数据库。你不能 JOIN。
根据查询方式设计数据，而非根据数据关系。
"""

// WRONG: Normalized (SQL thinking)
// users/{userId}
// posts/{postId} with authorId field
// To get "posts by user" - need to query posts collection

// RIGHT: Denormalized for queries
// users/{userId}/posts/{postId} - subcollection
// OR
// posts/{postId} with embedded author data

// Document structure for a post
const post = {
  id: 'post123',
  title: 'My Post',
  content: '...',

  // Embed frequently-needed author data
  author: {
    id: 'user456',
    name: 'Jane Doe',
    avatarUrl: '...'
  },

  // Arrays for IN queries (max 30 items for 'in')
  tags: ['javascript', 'firebase'],

  // Maps for compound queries
  stats: {
    likes: 42,
    comments: 7,
    views: 1000
  },

  // Timestamps
  createdAt: serverTimestamp(),
  updatedAt: serverTimestamp(),

  // Booleans for filtering
  published: true,
  featured: false
};

// Query patterns this enables:
// - Get post with author info: 1 read (no join needed)
// - Posts by tag: where('tags', 'array-contains', 'javascript')
// - Featured posts: where('featured', '==', true)
// - Recent posts: orderBy('createdAt', 'desc')

// When author updates their name, update all their posts
// This is the tradeoff: writes are more complex, reads are fast

### 实时监听器

订阅数据变更并正确清理

**何时使用**：实时功能

# REAL-TIME LISTENERS:

"""
onSnapshot 创建持久连接。组件卸载时务必取消订阅，
以防止内存泄漏和额外的读取操作。
"""

// React hook for real-time document
function useDocument(path) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const docRef = doc(db, path);

    // Subscribe to document
    const unsubscribe = onSnapshot(
      docRef,
      (snapshot) => {
        if (snapshot.exists()) {
          setData({ id: snapshot.id, ...snapshot.data() });
        } else {
          setData(null);
        }
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );

    // Cleanup on unmount
    return () => unsubscribe();
  }, [path]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }) {
  const { data: user, loading } = useDocument(`users/${userId}`);

  if (loading) return <Spinner />;
  return <div>{user?.name}</div>;
}

// Collection with query
function usePosts(limit = 10) {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const q = query(
      collection(db, 'posts'),
      where('published', '==', true),
      orderBy('createdAt', 'desc'),
      limit(limit)
    );

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const results = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setPosts(results);
    });

    return () => unsubscribe();
  }, [limit]);

  return posts;
}

### Cloud Functions 模式

使用 Cloud Functions v2 编写服务端逻辑

**何时使用**：后端逻辑、触发器、定时任务

# CLOUD FUNCTIONS V2:

"""
Cloud Functions 运行由事件触发的服务端代码。
V2 使用更标准的 Node.js 模式和更好的扩展性。
"""

import { onRequest } from 'firebase-functions/v2/https';
import { onDocumentCreated } from 'firebase-functions/v2/firestore';
import { onSchedule } from 'firebase-functions/v2/scheduler';
import { getFirestore } from 'firebase-admin/firestore';
import { initializeApp } from 'firebase-admin/app';

initializeApp();
const db = getFirestore();

// HTTP function
export const api = onRequest(
  { cors: true, region: 'us-central1' },
  async (req, res) => {
    // Verify auth token
    const token = req.headers.authorization?.split('Bearer ')[1];
    if (!token) {
      res.status(401).json({ error: 'Unauthorized' });
      return;
    }

    try {
      const decoded = await getAuth().verifyIdToken(token);
      // Process request with decoded.uid
      res.json({ userId: decoded.uid });
    } catch (error) {
      res.status(401).json({ error: 'Invalid token' });
    }
  }
);

// Firestore trigger - on document create
export const onUserCreated = onDocumentCreated(
  'users/{userId}',
  async (event) => {
    const snapshot = event.data;
    const userId = event.params.userId;

    if (!snapshot) return;

    const userData = snapshot.data();

    // Send welcome email, create related documents, etc.
    await db.collection('notifications').add({
      userId,
      type: 'welcome',
      message: `Welcome, ${userData.name}!`,
      createdAt: FieldValue.serverTimestamp()
    });
  }
);

// Scheduled function (every day at midnight)
export const dailyCleanup = onSchedule(
  { schedule: '0 0 * * *', timeZone: 'UTC' },
  async (event) => {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 30);

    // Delete old documents
    const oldDocs = await db.collection('logs')
      .where('createdAt', '<', cutoff)
      .limit(500)
      .get();

    const batch = db.batch();
    oldDocs.docs.forEach(doc => batch.delete(doc.ref));
    await batch.commit();

    console.log(`Deleted ${oldDocs.size} old logs`);
  }
);

### 批量操作

原子写入和事务保证一致性

**何时使用**：必须同时成功的多文档更新

# BATCH WRITES AND TRANSACTIONS:

"""
批量写入：多个写入操作要么全部成功，要么全部失败。
事务：读取后写入操作，保证一致性。
每个批量/事务最多 500 个操作。
"""

import {
  writeBatch, runTransaction, doc, getDoc,
  increment, serverTimestamp
} from 'firebase/firestore';

// Batch write - no reads, just writes
async function createPostWithTags(post, tags) {
  const batch = writeBatch(db);

  // Create post
  const postRef = doc(collection(db, 'posts'));
  batch.set(postRef, {
    ...post,
    createdAt: serverTimestamp()
  });

  // Update tag counts
  for (const tag of tags) {
    const tagRef = doc(db, 'tags', tag);
    batch.set(tagRef, {
      count: increment(1),
      lastUsed: serverTimestamp()
    }, { merge: true });
  }

  await batch.commit();
  return postRef.id;
}

// Transaction - read and write atomically
async function likePost(postId, userId) {
  return runTransaction(db, async (transaction) => {
    const postRef = doc(db, 'posts', postId);
    const likeRef = doc(db, 'posts', postId, 'likes', userId);

    const postSnap = await transaction.get(postRef);
    if (!postSnap.exists()) {
      throw new Error('Post not found');
    }

    const likeSnap = await transaction.get(likeRef);
    if (likeSnap.exists()) {
      throw new Error('Already liked');
    }

    // Increment like count and add like document
    transaction.update(postRef, {
      likeCount: increment(1)
    });

    transaction.set(likeRef, {
      userId,
      createdAt: serverTimestamp()
    });

    return postSnap.data().likeCount + 1;
  });
}

### 社交登录（Google、GitHub 等）

OAuth 提供商设置和认证流程

**何时使用**：社交登录实现

# SOCIAL LOGIN WITH FIREBASE AUTH

import {
  getAuth, signInWithPopup, signInWithRedirect,
  GoogleAuthProvider, GithubAuthProvider, OAuthProvider
} from "firebase/auth";

const auth = getAuth();

// GOOGLE
const googleProvider = new GoogleAuthProvider();
googleProvider.addScope("email");
googleProvider.setCustomParameters({ prompt: "select_account" });

async function signInWithGoogle() {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return result.user;
  } catch (error) {
    if (error.code === "auth/account-exists-with-different-credential") {
      return handleAccountConflict(error);
    }
    throw error;
  }
}

// GITHUB
const githubProvider = new GithubAuthProvider();
githubProvider.addScope("read:user");

// APPLE (Required for iOS apps!)
const appleProvider = new OAuthProvider("apple.com");
appleProvider.addScope("email");
appleProvider.addScope("name");

### 弹窗 vs 重定向认证

何时使用弹窗 vs 重定向进行 OAuth

**何时使用**：选择认证流程

# Popup: Desktop, SPA (simpler, can be blocked)
# Redirect: Mobile, iOS Safari (always works)

async function signIn(provider) {
  if (/iPhone|iPad|Android/i.test(navigator.userAgent)) {
    return signInWithRedirect(auth, provider);
  }
  try {
    return await signInWithPopup(auth, provider);
  } catch (e) {
    if (e.code === "auth/popup-blocked") {
      return signInWithRedirect(auth, provider);
    }
    throw e;
  }
}

// Check redirect result on page load
useEffect(() => {
  getRedirectResult(auth).then(r => r && setUser(r.user));
}, []);

### 账号关联

将多个提供商关联到一个账号

**何时使用**：用户有不同提供商的账号

import { fetchSignInMethodsForEmail, linkWithCredential } from "firebase/auth";

async function handleAccountConflict(error) {
  const email = error.customData?.email;
  const pendingCred = OAuthProvider.credentialFromError(error);
  const methods = await fetchSignInMethodsForEmail(auth, email);

  if (methods.includes("google.com")) {
    alert("Sign in with Google to link accounts");
    const result = await signInWithPopup(auth, new GoogleAuthProvider());
    await linkWithCredential(result.user, pendingCred);
    return result.user;
  }
}

// Link new provider
await linkWithPopup(auth.currentUser, new GithubAuthProvider());

// Unlink provider (keep at least one!)
await unlink(auth.currentUser, "github.com");

### 认证状态持久化

控制会话生命周期

**何时使用**：管理用户会话

import { setPersistence, browserLocalPersistence, browserSessionPersistence } from "firebase/auth";

// LOCAL: survives browser close (default)
// SESSION: cleared on tab close

async function signInWithRememberMe(email, pass, remember) {
  await setPersistence(auth, remember ? browserLocalPersistence : browserSessionPersistence);
  return signInWithEmailAndPassword(auth, email, pass);
}

// React auth hook
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => onAuthStateChanged(auth, u => { setUser(u); setLoading(false); }), []);
  return { user, loading };
}

### 邮箱验证和密码重置

完整的邮箱认证流程

**何时使用**：邮箱/密码认证

import { sendEmailVerification, sendPasswordResetEmail, reauthenticateWithCredential } from "firebase/auth";

// Sign up with verification
async function signUp(email, password) {
  const result = await createUserWithEmailAndPassword(auth, email, password);
  await sendEmailVerification(result.user);
  return result.user;
}

// Password reset
await sendPasswordResetEmail(auth, email);

// Change password (requires recent auth)
const cred = EmailAuthProvider.credential(user.email, currentPass);
await reauthenticateWithCredential(user, cred);
await updatePassword(user, newPass);

### API 的令牌管理

处理后端 API 调用的 ID 令牌

**何时使用**：与后端 API 认证

import { getIdToken, onIdTokenChanged } from "firebase/auth";

// Get token (auto-refreshes if expired)
const token = await getIdToken(auth.currentUser);

// API helper with auto-retry
async function apiCall(url, opts = {}) {
  const token = await getIdToken(auth.currentUser);
  const res = await fetch(url, {
    ...opts,
    headers: { ...opts.headers, Authorization: "Bearer " + token }
  });
  if (res.status === 401) {
    const newToken = await getIdToken(auth.currentUser, true);
    return fetch(url, { ...opts, headers: { ...opts.headers, Authorization: "Bearer " + newToken }});
  }
  return res;
}

// Sync to cookie for SSR
onIdTokenChanged(auth, async u => {
  document.cookie = u ? "__session=" + await u.getIdToken() : "__session=; max-age=0";
});

// Check admin claim
const { claims } = await auth.currentUser.getIdTokenResult();
const isAdmin = claims.admin === true;

## 协作

### 委托触发器

- user needs complex OAuth flow -> authentication-oauth（Firebase Auth 处理基础，复杂流程需要 OAuth 技能）
- user needs payment integration -> stripe（Firebase + Stripe 是常见组合）
- user needs email functionality -> email（Firebase 不包含邮件——使用 SendGrid、Resend 等）
- user needs container deployment -> devops（超出 Firebase Hosting 范围——Kubernetes、Docker）
- user needs relational data model -> postgres-wizard（Firestore 不是高度关系型数据的正确选择）
- user needs full-text search -> elasticsearch-search（Firestore 不支持全文搜索——使用 Algolia/Elastic）

## 相关技能

配合使用：`nextjs-app-router`、`react-patterns`、`authentication-oauth`、`stripe`

## 何时使用

- 用户提及或暗示：firebase
- 用户提及或暗示：firestore
- 用户提及或暗示：firebase auth
- 用户提及或暗示：cloud functions
- 用户提及或暗示：firebase storage
- 用户提及或暗示：realtime database
- 用户提及或暗示：firebase hosting
- 用户提及或暗示：firebase emulator
- 用户提及或暗示：security rules
- 用户提及或暗示：firebase admin

## 局限性

- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
