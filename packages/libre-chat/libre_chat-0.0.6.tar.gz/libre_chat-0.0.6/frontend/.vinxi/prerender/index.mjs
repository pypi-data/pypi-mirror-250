globalThis._importMeta_={url:import.meta.url,env:process.env};import 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/node-fetch-native@1.6.1/node_modules/node-fetch-native/dist/polyfill.cjs';
import { defineEventHandler, handleCacheHeaders, splitCookiesString, isEvent, createEvent, getRequestHeader, eventHandler, setHeaders, sendRedirect, proxyRequest, setResponseStatus, setResponseHeader, send, removeResponseHeader, createError, getResponseHeader, setHeader, toWebRequest, getRequestIP, appendResponseHeader, getCookie, setCookie, createApp, createRouter as createRouter$1, toNodeListener, fetchWithEvent, lazyEventHandler } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/h3@1.9.0/node_modules/h3/dist/index.mjs';
import { createFetch as createFetch$1, Headers as Headers$1 } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/ofetch@1.3.3/node_modules/ofetch/dist/node.mjs';
import destr from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/destr@2.0.2/node_modules/destr/dist/index.mjs';
import { createCall, createFetch } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/unenv@1.9.0/node_modules/unenv/runtime/fetch/index.mjs';
import { createHooks } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/hookable@5.5.3/node_modules/hookable/dist/index.mjs';
import { snakeCase } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/scule@1.1.1/node_modules/scule/dist/index.mjs';
import { klona } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/klona@2.0.6/node_modules/klona/dist/index.mjs';
import defu, { defuFn } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/defu@6.1.4/node_modules/defu/dist/defu.mjs';
import { hash } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/ohash@1.1.3/node_modules/ohash/dist/index.mjs';
import { parseURL, withoutBase, joinURL, getQuery, withQuery, decodePath, withLeadingSlash, withoutTrailingSlash } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/ufo@1.3.2/node_modules/ufo/dist/index.mjs';
import { createStorage, prefixStorage } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/unstorage@1.10.1/node_modules/unstorage/dist/index.mjs';
import unstorage_47drivers_47fs from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/unstorage@1.10.1/node_modules/unstorage/drivers/fs.mjs';
import unstorage_47drivers_47fs_45lite from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/unstorage@1.10.1/node_modules/unstorage/drivers/fs-lite.mjs';
import { toRouteMatcher, createRouter } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/radix3@1.1.0/node_modules/radix3/dist/index.mjs';
import _pPG8r2IIAA from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/vinxi@0.1.1_preact@10.19.3/node_modules/vinxi/lib/app-fetch.js';
import _M6z7Kmp2oz from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/vinxi@0.1.1_preact@10.19.3/node_modules/vinxi/lib/app-manifest.js';
import { promises } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/pathe@1.1.1/node_modules/pathe/dist/index.mjs';
import { sharedConfig, lazy, createComponent as createComponent$1 } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/solid-js@1.8.8/node_modules/solid-js/dist/server.js';
import { provideRequestEvent } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/solid-js@1.8.8/node_modules/solid-js/web/dist/storage.js';
import { ssr, renderToStream, createComponent, ssrHydrationKey, NoHydration, escape, getRequestEvent, ssrAttribute, ssrElement, mergeProps } from 'file:///home/vemonet/dev/llm/libre-chat/frontend/node_modules/.pnpm/solid-js@1.8.8/node_modules/solid-js/web/dist/server.js';

const inlineAppConfig = {};



const appConfig$1 = defuFn(inlineAppConfig);

const _inlineRuntimeConfig = {
  "app": {
    "baseURL": "/"
  },
  "nitro": {
    "routeRules": {}
  }
};
const ENV_PREFIX = "NITRO_";
const ENV_PREFIX_ALT = _inlineRuntimeConfig.nitro.envPrefix ?? process.env.NITRO_ENV_PREFIX ?? "_";
const _sharedRuntimeConfig = _deepFreeze(
  _applyEnv(klona(_inlineRuntimeConfig))
);
function useRuntimeConfig(event) {
  if (!event) {
    return _sharedRuntimeConfig;
  }
  if (event.context.nitro.runtimeConfig) {
    return event.context.nitro.runtimeConfig;
  }
  const runtimeConfig = klona(_inlineRuntimeConfig);
  _applyEnv(runtimeConfig);
  event.context.nitro.runtimeConfig = runtimeConfig;
  return runtimeConfig;
}
_deepFreeze(klona(appConfig$1));
function _getEnv(key) {
  const envKey = snakeCase(key).toUpperCase();
  return destr(
    process.env[ENV_PREFIX + envKey] ?? process.env[ENV_PREFIX_ALT + envKey]
  );
}
function _isObject(input) {
  return typeof input === "object" && !Array.isArray(input);
}
function _applyEnv(obj, parentKey = "") {
  for (const key in obj) {
    const subKey = parentKey ? `${parentKey}_${key}` : key;
    const envValue = _getEnv(subKey);
    if (_isObject(obj[key])) {
      if (_isObject(envValue)) {
        obj[key] = { ...obj[key], ...envValue };
      }
      _applyEnv(obj[key], subKey);
    } else {
      obj[key] = envValue ?? obj[key];
    }
  }
  return obj;
}
function _deepFreeze(object) {
  const propNames = Object.getOwnPropertyNames(object);
  for (const name of propNames) {
    const value = object[name];
    if (value && typeof value === "object") {
      _deepFreeze(value);
    }
  }
  return Object.freeze(object);
}
new Proxy(/* @__PURE__ */ Object.create(null), {
  get: (_, prop) => {
    console.warn(
      "Please use `useRuntimeConfig()` instead of accessing config directly."
    );
    const runtimeConfig = useRuntimeConfig();
    if (prop in runtimeConfig) {
      return runtimeConfig[prop];
    }
    return void 0;
  }
});

const serverAssets = [{"baseName":"server","dir":"/home/vemonet/dev/llm/libre-chat/frontend/assets"}];

const assets$1 = createStorage();

for (const asset of serverAssets) {
  assets$1.mount(asset.baseName, unstorage_47drivers_47fs({ base: asset.dir }));
}

const storage = createStorage({});

storage.mount('/assets', assets$1);

storage.mount('data', unstorage_47drivers_47fs_45lite({"driver":"fsLite","base":"/home/vemonet/dev/llm/libre-chat/frontend/.data/kv"}));
storage.mount('root', unstorage_47drivers_47fs({"driver":"fs","readOnly":true,"base":"/home/vemonet/dev/llm/libre-chat/frontend","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('src', unstorage_47drivers_47fs({"driver":"fs","readOnly":true,"base":"/home/vemonet/dev/llm/libre-chat/frontend","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('build', unstorage_47drivers_47fs({"driver":"fs","readOnly":false,"base":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('cache', unstorage_47drivers_47fs({"driver":"fs","readOnly":false,"base":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi/cache","ignore":["**/node_modules/**","**/.git/**"]}));

function useStorage(base = "") {
  return base ? prefixStorage(storage, base) : storage;
}

const defaultCacheOptions = {
  name: "_",
  base: "/cache",
  swr: true,
  maxAge: 1
};
function defineCachedFunction(fn, opts = {}) {
  opts = { ...defaultCacheOptions, ...opts };
  const pending = {};
  const group = opts.group || "nitro/functions";
  const name = opts.name || fn.name || "_";
  const integrity = opts.integrity || hash([fn, opts]);
  const validate = opts.validate || ((entry) => entry.value !== void 0);
  async function get(key, resolver, shouldInvalidateCache, event) {
    const cacheKey = [opts.base, group, name, key + ".json"].filter(Boolean).join(":").replace(/:\/$/, ":index");
    const entry = await useStorage().getItem(cacheKey) || {};
    const ttl = (opts.maxAge ?? opts.maxAge ?? 0) * 1e3;
    if (ttl) {
      entry.expires = Date.now() + ttl;
    }
    const expired = shouldInvalidateCache || entry.integrity !== integrity || ttl && Date.now() - (entry.mtime || 0) > ttl || validate(entry) === false;
    const _resolve = async () => {
      const isPending = pending[key];
      if (!isPending) {
        if (entry.value !== void 0 && (opts.staleMaxAge || 0) >= 0 && opts.swr === false) {
          entry.value = void 0;
          entry.integrity = void 0;
          entry.mtime = void 0;
          entry.expires = void 0;
        }
        pending[key] = Promise.resolve(resolver());
      }
      try {
        entry.value = await pending[key];
      } catch (error) {
        if (!isPending) {
          delete pending[key];
        }
        throw error;
      }
      if (!isPending) {
        entry.mtime = Date.now();
        entry.integrity = integrity;
        delete pending[key];
        if (validate(entry) !== false) {
          const promise = useStorage().setItem(cacheKey, entry).catch((error) => {
            console.error(`[nitro] [cache] Cache write error.`, error);
            useNitroApp().captureError(error, { event, tags: ["cache"] });
          });
          if (event && event.waitUntil) {
            event.waitUntil(promise);
          }
        }
      }
    };
    const _resolvePromise = expired ? _resolve() : Promise.resolve();
    if (entry.value === void 0) {
      await _resolvePromise;
    } else if (expired && event && event.waitUntil) {
      event.waitUntil(_resolvePromise);
    }
    if (opts.swr && validate(entry) !== false) {
      _resolvePromise.catch((error) => {
        console.error(`[nitro] [cache] SWR handler error.`, error);
        useNitroApp().captureError(error, { event, tags: ["cache"] });
      });
      return entry;
    }
    return _resolvePromise.then(() => entry);
  }
  return async (...args) => {
    const shouldBypassCache = opts.shouldBypassCache?.(...args);
    if (shouldBypassCache) {
      return fn(...args);
    }
    const key = await (opts.getKey || getKey)(...args);
    const shouldInvalidateCache = opts.shouldInvalidateCache?.(...args);
    const entry = await get(
      key,
      () => fn(...args),
      shouldInvalidateCache,
      args[0] && isEvent(args[0]) ? args[0] : void 0
    );
    let value = entry.value;
    if (opts.transform) {
      value = await opts.transform(entry, ...args) || value;
    }
    return value;
  };
}
const cachedFunction = defineCachedFunction;
function getKey(...args) {
  return args.length > 0 ? hash(args, {}) : "";
}
function escapeKey(key) {
  return String(key).replace(/\W/g, "");
}
function defineCachedEventHandler(handler, opts = defaultCacheOptions) {
  const variableHeaderNames = (opts.varies || []).filter(Boolean).map((h) => h.toLowerCase()).sort();
  const _opts = {
    ...opts,
    getKey: async (event) => {
      const customKey = await opts.getKey?.(event);
      if (customKey) {
        return escapeKey(customKey);
      }
      const _path = event.node.req.originalUrl || event.node.req.url || event.path;
      const _pathname = escapeKey(decodeURI(parseURL(_path).pathname)).slice(0, 16) || "index";
      const _hashedPath = `${_pathname}.${hash(_path)}`;
      const _headers = variableHeaderNames.map((header) => [header, event.node.req.headers[header]]).map(([name, value]) => `${escapeKey(name)}.${hash(value)}`);
      return [_hashedPath, ..._headers].join(":");
    },
    validate: (entry) => {
      if (!entry.value) {
        return false;
      }
      if (entry.value.code >= 400) {
        return false;
      }
      if (entry.value.body === void 0) {
        return false;
      }
      if (entry.value.headers.etag === "undefined" || entry.value.headers["last-modified"] === "undefined") {
        return false;
      }
      return true;
    },
    group: opts.group || "nitro/handlers",
    integrity: opts.integrity || hash([handler, opts])
  };
  const _cachedHandler = cachedFunction(
    async (incomingEvent) => {
      const variableHeaders = {};
      for (const header of variableHeaderNames) {
        variableHeaders[header] = incomingEvent.node.req.headers[header];
      }
      const reqProxy = cloneWithProxy(incomingEvent.node.req, {
        headers: variableHeaders
      });
      const resHeaders = {};
      let _resSendBody;
      const resProxy = cloneWithProxy(incomingEvent.node.res, {
        statusCode: 200,
        writableEnded: false,
        writableFinished: false,
        headersSent: false,
        closed: false,
        getHeader(name) {
          return resHeaders[name];
        },
        setHeader(name, value) {
          resHeaders[name] = value;
          return this;
        },
        getHeaderNames() {
          return Object.keys(resHeaders);
        },
        hasHeader(name) {
          return name in resHeaders;
        },
        removeHeader(name) {
          delete resHeaders[name];
        },
        getHeaders() {
          return resHeaders;
        },
        end(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2();
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return this;
        },
        write(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2();
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return this;
        },
        writeHead(statusCode, headers2) {
          this.statusCode = statusCode;
          if (headers2) {
            for (const header in headers2) {
              this.setHeader(header, headers2[header]);
            }
          }
          return this;
        }
      });
      const event = createEvent(reqProxy, resProxy);
      event.context = incomingEvent.context;
      const body = await handler(event) || _resSendBody;
      const headers = event.node.res.getHeaders();
      headers.etag = String(
        headers.Etag || headers.etag || `W/"${hash(body)}"`
      );
      headers["last-modified"] = String(
        headers["Last-Modified"] || headers["last-modified"] || (/* @__PURE__ */ new Date()).toUTCString()
      );
      const cacheControl = [];
      if (opts.swr) {
        if (opts.maxAge) {
          cacheControl.push(`s-maxage=${opts.maxAge}`);
        }
        if (opts.staleMaxAge) {
          cacheControl.push(`stale-while-revalidate=${opts.staleMaxAge}`);
        } else {
          cacheControl.push("stale-while-revalidate");
        }
      } else if (opts.maxAge) {
        cacheControl.push(`max-age=${opts.maxAge}`);
      }
      if (cacheControl.length > 0) {
        headers["cache-control"] = cacheControl.join(", ");
      }
      const cacheEntry = {
        code: event.node.res.statusCode,
        headers,
        body
      };
      return cacheEntry;
    },
    _opts
  );
  return defineEventHandler(async (event) => {
    if (opts.headersOnly) {
      if (handleCacheHeaders(event, { maxAge: opts.maxAge })) {
        return;
      }
      return handler(event);
    }
    const response = await _cachedHandler(event);
    if (event.node.res.headersSent || event.node.res.writableEnded) {
      return response.body;
    }
    if (handleCacheHeaders(event, {
      modifiedTime: new Date(response.headers["last-modified"]),
      etag: response.headers.etag,
      maxAge: opts.maxAge
    })) {
      return;
    }
    event.node.res.statusCode = response.code;
    for (const name in response.headers) {
      const value = response.headers[name];
      if (name === "set-cookie") {
        event.node.res.appendHeader(
          name,
          splitCookiesString(value)
        );
      } else {
        event.node.res.setHeader(name, value);
      }
    }
    return response.body;
  });
}
function cloneWithProxy(obj, overrides) {
  return new Proxy(obj, {
    get(target, property, receiver) {
      if (property in overrides) {
        return overrides[property];
      }
      return Reflect.get(target, property, receiver);
    },
    set(target, property, value, receiver) {
      if (property in overrides) {
        overrides[property] = value;
        return true;
      }
      return Reflect.set(target, property, value, receiver);
    }
  });
}
const cachedEventHandler = defineCachedEventHandler;

function hasReqHeader(event, name, includes) {
  const value = getRequestHeader(event, name);
  return value && typeof value === "string" && value.toLowerCase().includes(includes);
}
function isJsonRequest(event) {
  if (hasReqHeader(event, "accept", "text/html")) {
    return false;
  }
  return hasReqHeader(event, "accept", "application/json") || hasReqHeader(event, "user-agent", "curl/") || hasReqHeader(event, "user-agent", "httpie/") || hasReqHeader(event, "sec-fetch-mode", "cors") || event.path.startsWith("/api/") || event.path.endsWith(".json");
}
function normalizeError(error) {
  const cwd = typeof process.cwd === "function" ? process.cwd() : "/";
  const stack = (error.stack || "").split("\n").splice(1).filter((line) => line.includes("at ")).map((line) => {
    const text = line.replace(cwd + "/", "./").replace("webpack:/", "").replace("file://", "").trim();
    return {
      text,
      internal: line.includes("node_modules") && !line.includes(".cache") || line.includes("internal") || line.includes("new Promise")
    };
  });
  const statusCode = error.statusCode || 500;
  const statusMessage = error.statusMessage ?? (statusCode === 404 ? "Not Found" : "");
  const message = error.message || error.toString();
  return {
    stack,
    statusCode,
    statusMessage,
    message
  };
}
function _captureError(error, type) {
  console.error(`[nitro] [${type}]`, error);
  useNitroApp().captureError(error, { tags: [type] });
}
function trapUnhandledNodeErrors() {
  process.on(
    "unhandledRejection",
    (error) => _captureError(error, "unhandledRejection")
  );
  process.on(
    "uncaughtException",
    (error) => _captureError(error, "uncaughtException")
  );
}
function joinHeaders(value) {
  return Array.isArray(value) ? value.join(", ") : String(value);
}
function normalizeFetchResponse(response) {
  if (!response.headers.has("set-cookie")) {
    return response;
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: normalizeCookieHeaders(response.headers)
  });
}
function normalizeCookieHeader(header = "") {
  return splitCookiesString(joinHeaders(header));
}
function normalizeCookieHeaders(headers) {
  const outgoingHeaders = new Headers();
  for (const [name, header] of headers) {
    if (name === "set-cookie") {
      for (const cookie of normalizeCookieHeader(header)) {
        outgoingHeaders.append("set-cookie", cookie);
      }
    } else {
      outgoingHeaders.set(name, joinHeaders(header));
    }
  }
  return outgoingHeaders;
}

const config = useRuntimeConfig();
const _routeRulesMatcher = toRouteMatcher(
  createRouter({ routes: config.nitro.routeRules })
);
function createRouteRulesHandler(ctx) {
  return eventHandler((event) => {
    const routeRules = getRouteRules(event);
    if (routeRules.headers) {
      setHeaders(event, routeRules.headers);
    }
    if (routeRules.redirect) {
      return sendRedirect(
        event,
        routeRules.redirect.to,
        routeRules.redirect.statusCode
      );
    }
    if (routeRules.proxy) {
      let target = routeRules.proxy.to;
      if (target.endsWith("/**")) {
        let targetPath = event.path;
        const strpBase = routeRules.proxy._proxyStripBase;
        if (strpBase) {
          targetPath = withoutBase(targetPath, strpBase);
        }
        target = joinURL(target.slice(0, -3), targetPath);
      } else if (event.path.includes("?")) {
        const query = getQuery(event.path);
        target = withQuery(target, query);
      }
      return proxyRequest(event, target, {
        fetch: ctx.localFetch,
        ...routeRules.proxy
      });
    }
  });
}
function getRouteRules(event) {
  event.context._nitro = event.context._nitro || {};
  if (!event.context._nitro.routeRules) {
    event.context._nitro.routeRules = getRouteRulesForPath(
      withoutBase(event.path.split("?")[0], useRuntimeConfig().app.baseURL)
    );
  }
  return event.context._nitro.routeRules;
}
function getRouteRulesForPath(path) {
  return defu({}, ..._routeRulesMatcher.matchAll(path).reverse());
}

const appConfig = {"name":"vinxi","routers":[{"name":"public","mode":"static","dir":"./public","base":"/","root":"/home/vemonet/dev/llm/libre-chat/frontend","order":0,"outDir":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi/build/public"},{"name":"ssr","mode":"handler","handler":"src/entry-server.tsx","extensions":["js","jsx","ts","tsx"],"target":"server","root":"/home/vemonet/dev/llm/libre-chat/frontend","base":"/","outDir":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi/build/ssr","order":1},{"name":"client","mode":"build","handler":"src/entry-client.tsx","extensions":["js","jsx","ts","tsx"],"target":"browser","base":"/_build","root":"/home/vemonet/dev/llm/libre-chat/frontend","outDir":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi/build/client","order":2},{"name":"server-fns","mode":"handler","base":"/_server","handler":"node_modules/.pnpm/@solidjs+start@0.4.4_solid-js@1.8.8_vinxi@0.1.1_vite@5.0.11/node_modules/@solidjs/start/config/server-handler.js","target":"server","root":"/home/vemonet/dev/llm/libre-chat/frontend","outDir":"/home/vemonet/dev/llm/libre-chat/frontend/.vinxi/build/server-fns","order":3}],"server":{"compressPublicAssets":{"brotli":true},"prerender":{}},"root":"/home/vemonet/dev/llm/libre-chat/frontend"};
				const buildManifest = {"ssr":{"_components-86ea9901.js":{"file":"assets/components-86ea9901.js"},"_routes-52c4f9a3.js":{"dynamicImports":["src/routes/[...404].tsx?pick=default&pick=$css","src/routes/[...404].tsx?pick=default&pick=$css","src/routes/about.tsx?pick=default&pick=$css","src/routes/about.tsx?pick=default&pick=$css","src/routes/index.tsx?pick=default&pick=$css","src/routes/index.tsx?pick=default&pick=$css"],"file":"assets/routes-52c4f9a3.js"},"src/routes/[...404].tsx?pick=default&pick=$css":{"file":"_...404_.js","imports":["_components-86ea9901.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/[...404].tsx?pick=default&pick=$css"},"src/routes/about.tsx?pick=default&pick=$css":{"file":"about.js","imports":["_components-86ea9901.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/about.tsx?pick=default&pick=$css"},"src/routes/index.css":{"file":"assets/index-cc63fe87.css","src":"src/routes/index.css"},"src/routes/index.tsx?pick=default&pick=$css":{"css":["assets/index-cc63fe87.css"],"file":"index.js","imports":["_routes-52c4f9a3.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/index.tsx?pick=default&pick=$css"},"virtual:#vinxi/handler/ssr":{"file":"ssr.js","imports":["_routes-52c4f9a3.js"],"isEntry":true,"src":"virtual:#vinxi/handler/ssr"}},"client":{"_app-e5fa8b0c.js":{"css":["assets/app-cc63fe87.css"],"dynamicImports":["src/routes/[...404].tsx?pick=default&pick=$css","src/routes/about.tsx?pick=default&pick=$css","src/routes/index.tsx?pick=default&pick=$css"],"file":"assets/app-e5fa8b0c.js","imports":["_routing-e8757775.js"]},"_components-70d2ff75.js":{"file":"assets/components-70d2ff75.js","imports":["_routing-e8757775.js"]},"_routing-e8757775.js":{"file":"assets/routing-e8757775.js"},"app.css":{"file":"assets/app-cc63fe87.css","src":"app.css"},"src/routes/[...404].tsx?pick=default&pick=$css":{"file":"assets/_...404_-8a5712b0.js","imports":["_routing-e8757775.js","_components-70d2ff75.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/[...404].tsx?pick=default&pick=$css"},"src/routes/about.tsx?pick=default&pick=$css":{"file":"assets/about-cf4c1418.js","imports":["_routing-e8757775.js","_components-70d2ff75.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/about.tsx?pick=default&pick=$css"},"src/routes/index.tsx?pick=default&pick=$css":{"file":"assets/index-aae57daf.js","imports":["_routing-e8757775.js","_app-e5fa8b0c.js"],"isDynamicEntry":true,"isEntry":true,"src":"src/routes/index.tsx?pick=default&pick=$css"},"virtual:#vinxi/handler/client":{"file":"assets/client-81bb5258.js","imports":["_routing-e8757775.js","_app-e5fa8b0c.js"],"isEntry":true,"src":"virtual:#vinxi/handler/client"}},"server-fns":{"virtual:#vinxi/handler/server-fns":{"file":"entry.js","isEntry":true,"src":"virtual:#vinxi/handler/server-fns"}}};

				const routeManifest = {"ssr":{},"client":{}};

        function createProdApp(appConfig) {
          return {
            config: { ...appConfig, buildManifest, routeManifest },
            getRouter(name) {
              return appConfig.routers.find(router => router.name === name)
            }
          }
        }

        function plugin(app) {
          const prodApp = createProdApp(appConfig);
          globalThis.app = prodApp;
        }

const chunks = {};
			 



			 function app() {
				 globalThis.$$chunks = chunks;
			 }

const plugins = [
  plugin,
_pPG8r2IIAA,
_M6z7Kmp2oz,
app
];

function defineNitroErrorHandler(handler) {
  return handler;
}
const errorHandler = defineNitroErrorHandler(
  function defaultNitroErrorHandler(error, event) {
    const { stack, statusCode, statusMessage, message } = normalizeError(error);
    const errorObject = {
      url: event.path || "",
      statusCode,
      statusMessage,
      message,
      stack: void 0
    };
    if (error.unhandled || error.fatal) {
      const tags = [
        "[nitro]",
        "[request error]",
        error.unhandled && "[unhandled]",
        error.fatal && "[fatal]"
      ].filter(Boolean).join(" ");
      console.error(
        tags,
        error.message + "\n" + stack.map((l) => "  " + l.text).join("  \n")
      );
    }
    setResponseStatus(event, statusCode, statusMessage);
    if (isJsonRequest(event)) {
      setResponseHeader(event, "Content-Type", "application/json");
      return send(event, JSON.stringify(errorObject));
    } else {
      setResponseHeader(event, "Content-Type", "text/html");
      return send(event, renderHTMLError(errorObject));
    }
  }
);
function renderHTMLError(error) {
  const statusCode = error.statusCode || 500;
  const statusMessage = error.statusMessage || "Request Error";
  return `<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${statusCode} ${statusMessage}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico/css/pico.min.css">
  </head>
  <body>
    <main class="container">
      <dialog open>
        <article>
          <header>
            <h2>${statusCode} ${statusMessage}</h2>
          </header>
          <code>
            ${error.message}<br><br>
            ${"\n" + (error.stack || []).map((i) => `&nbsp;&nbsp;${i}`).join("<br>")}
          </code>
          <footer>
            <a href="/" onclick="event.preventDefault();history.back();">Go Back</a>
          </footer>
        </article>
      </dialog>
    </main>
  </body>
</html>
`;
}

const assets = {
  "/favicon.ico": {
    "type": "image/vnd.microsoft.icon",
    "etag": "\"3c2e-z+DSU7IaT33iENhIyvmf0Kdb6cM\"",
    "mtime": "2024-01-08T00:18:01.604Z",
    "size": 15406,
    "path": "../../.output/public/favicon.ico"
  },
  "/_build/manifest.json": {
    "type": "application/json",
    "etag": "\"6d0-u4xdZ+/UuXnXYtct+gnX089sFZM\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 1744,
    "path": "../../.output/public/_build/manifest.json"
  },
  "/_build/manifest.json.br": {
    "type": "application/json",
    "encoding": "br",
    "etag": "\"15a-HzpUOUyBsOEiffL/tnkJDiJJAmQ\"",
    "mtime": "2024-01-08T00:18:01.696Z",
    "size": 346,
    "path": "../../.output/public/_build/manifest.json.br"
  },
  "/_build/manifest.json.gz": {
    "type": "application/json",
    "encoding": "gzip",
    "etag": "\"18d-2jBcIAVanSOa/zwK0ER7Ulr8IpY\"",
    "mtime": "2024-01-08T00:18:01.672Z",
    "size": 397,
    "path": "../../.output/public/_build/manifest.json.gz"
  },
  "/_build/server-functions-manifest.json": {
    "type": "application/json",
    "etag": "\"19-U+evudgPW1yE9kGumdxd/vtvk2s\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 25,
    "path": "../../.output/public/_build/server-functions-manifest.json"
  },
  "/assets/components-86ea9901.js": {
    "type": "application/javascript",
    "etag": "\"4af-qXVx/EU750ZRllfZ9ZNxEkMKrpU\"",
    "mtime": "2024-01-08T00:18:01.616Z",
    "size": 1199,
    "path": "../../.output/public/assets/components-86ea9901.js"
  },
  "/assets/components-86ea9901.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"25a-AI/pjiL2CPUG4VwVHrLmExPQyOU\"",
    "mtime": "2024-01-08T00:18:01.684Z",
    "size": 602,
    "path": "../../.output/public/assets/components-86ea9901.js.br"
  },
  "/assets/components-86ea9901.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"2a2-Tb0yjJgrkqulwINKPMhMIZgVQXI\"",
    "mtime": "2024-01-08T00:18:01.672Z",
    "size": 674,
    "path": "../../.output/public/assets/components-86ea9901.js.gz"
  },
  "/assets/index-cc63fe87.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"9dbe-hBjR8ITiuERkfI2lGs8njDjAJP0\"",
    "mtime": "2024-01-08T00:18:01.616Z",
    "size": 40382,
    "path": "../../.output/public/assets/index-cc63fe87.css"
  },
  "/assets/index-cc63fe87.css.br": {
    "type": "text/css; charset=utf-8",
    "encoding": "br",
    "etag": "\"19ab-wjA0Z+wogxTdgbhxz2vT6PXLdDM\"",
    "mtime": "2024-01-08T00:18:01.960Z",
    "size": 6571,
    "path": "../../.output/public/assets/index-cc63fe87.css.br"
  },
  "/assets/index-cc63fe87.css.gz": {
    "type": "text/css; charset=utf-8",
    "encoding": "gzip",
    "etag": "\"1d5f-hWfKnDN47LFvsVIEx+NJJdvdMnA\"",
    "mtime": "2024-01-08T00:18:01.696Z",
    "size": 7519,
    "path": "../../.output/public/assets/index-cc63fe87.css.gz"
  },
  "/assets/routes-52c4f9a3.js": {
    "type": "application/javascript",
    "etag": "\"8bd-2BuhKC7aMVkdZAYd9jGYz/fb6eA\"",
    "mtime": "2024-01-08T00:18:01.616Z",
    "size": 2237,
    "path": "../../.output/public/assets/routes-52c4f9a3.js"
  },
  "/assets/routes-52c4f9a3.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"37d-TXzd/Mae1MpFLO6ygU13nMth8nQ\"",
    "mtime": "2024-01-08T00:18:01.692Z",
    "size": 893,
    "path": "../../.output/public/assets/routes-52c4f9a3.js.br"
  },
  "/assets/routes-52c4f9a3.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"3d7-E0+ntO9BC8VyIG8GRdF+YhwyfHU\"",
    "mtime": "2024-01-08T00:18:01.676Z",
    "size": 983,
    "path": "../../.output/public/assets/routes-52c4f9a3.js.gz"
  },
  "/_build/assets/_...404_-8a5712b0.js": {
    "type": "application/javascript",
    "etag": "\"2cf-t1IcNtSSbGcvdD/Zgen1TQY636M\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 719,
    "path": "../../.output/public/_build/assets/_...404_-8a5712b0.js"
  },
  "/_build/assets/about-cf4c1418.js": {
    "type": "application/javascript",
    "etag": "\"3c5-RVYYsPnRqkynpLH4Mp1xWjSHNow\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 965,
    "path": "../../.output/public/_build/assets/about-cf4c1418.js"
  },
  "/_build/assets/app-cc63fe87.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"9dbe-hBjR8ITiuERkfI2lGs8njDjAJP0\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 40382,
    "path": "../../.output/public/_build/assets/app-cc63fe87.css"
  },
  "/_build/assets/app-cc63fe87.css.br": {
    "type": "text/css; charset=utf-8",
    "encoding": "br",
    "etag": "\"19ab-wjA0Z+wogxTdgbhxz2vT6PXLdDM\"",
    "mtime": "2024-01-08T00:18:01.896Z",
    "size": 6571,
    "path": "../../.output/public/_build/assets/app-cc63fe87.css.br"
  },
  "/_build/assets/app-cc63fe87.css.gz": {
    "type": "text/css; charset=utf-8",
    "encoding": "gzip",
    "etag": "\"1d5f-hWfKnDN47LFvsVIEx+NJJdvdMnA\"",
    "mtime": "2024-01-08T00:18:01.760Z",
    "size": 7519,
    "path": "../../.output/public/_build/assets/app-cc63fe87.css.gz"
  },
  "/_build/assets/app-e5fa8b0c.js": {
    "type": "application/javascript",
    "etag": "\"308b-WcYmvmlB/TlwQrh8J3Ru0q6dVJo\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 12427,
    "path": "../../.output/public/_build/assets/app-e5fa8b0c.js"
  },
  "/_build/assets/app-e5fa8b0c.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"106d-KUgdp7nlKy5oCgeIumaCxd8eKBs\"",
    "mtime": "2024-01-08T00:18:01.760Z",
    "size": 4205,
    "path": "../../.output/public/_build/assets/app-e5fa8b0c.js.br"
  },
  "/_build/assets/app-e5fa8b0c.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"1296-t6fHN/d7wZ2S58m5lMw0hPXgOQs\"",
    "mtime": "2024-01-08T00:18:01.724Z",
    "size": 4758,
    "path": "../../.output/public/_build/assets/app-e5fa8b0c.js.gz"
  },
  "/_build/assets/client-81bb5258.js": {
    "type": "application/javascript",
    "etag": "\"a09-Q460OMxXZjDQ5PdnWn1SB4R1x2U\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 2569,
    "path": "../../.output/public/_build/assets/client-81bb5258.js"
  },
  "/_build/assets/client-81bb5258.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"461-B4X85nfaR2rIiC0ZC0PHnzp2nG4\"",
    "mtime": "2024-01-08T00:18:01.724Z",
    "size": 1121,
    "path": "../../.output/public/_build/assets/client-81bb5258.js.br"
  },
  "/_build/assets/client-81bb5258.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"4f6-sfAanL+i9sQSVOsh6YdP68FCCHA\"",
    "mtime": "2024-01-08T00:18:01.724Z",
    "size": 1270,
    "path": "../../.output/public/_build/assets/client-81bb5258.js.gz"
  },
  "/_build/assets/components-70d2ff75.js": {
    "type": "application/javascript",
    "etag": "\"2ef-HvBDPx5ayr0PWjm+8Ea8xI+zTsA\"",
    "mtime": "2024-01-08T00:18:01.636Z",
    "size": 751,
    "path": "../../.output/public/_build/assets/components-70d2ff75.js"
  },
  "/_build/assets/index-aae57daf.js": {
    "type": "application/javascript",
    "etag": "\"9aa4-fzBSff0kb5OE6Vgy3HMUpaNzcYE\"",
    "mtime": "2024-01-08T00:18:01.640Z",
    "size": 39588,
    "path": "../../.output/public/_build/assets/index-aae57daf.js"
  },
  "/_build/assets/index-aae57daf.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"2e33-Tx0TFPw9GveuB8CH4wj1MyGBaYQ\"",
    "mtime": "2024-01-08T00:18:02.020Z",
    "size": 11827,
    "path": "../../.output/public/_build/assets/index-aae57daf.js.br"
  },
  "/_build/assets/index-aae57daf.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"3247-93A4seUcT7A0RBqC9S+zs0tcSKM\"",
    "mtime": "2024-01-08T00:18:01.896Z",
    "size": 12871,
    "path": "../../.output/public/_build/assets/index-aae57daf.js.gz"
  },
  "/_build/assets/routing-e8757775.js": {
    "type": "application/javascript",
    "etag": "\"724d-Imf1bXPjG46yrgCn8HYD1V/PEoI\"",
    "mtime": "2024-01-08T00:18:01.640Z",
    "size": 29261,
    "path": "../../.output/public/_build/assets/routing-e8757775.js"
  },
  "/_build/assets/routing-e8757775.js.br": {
    "type": "application/javascript",
    "encoding": "br",
    "etag": "\"295c-jn7KE94wWyguwVGNbnT81wbnYI4\"",
    "mtime": "2024-01-08T00:18:01.936Z",
    "size": 10588,
    "path": "../../.output/public/_build/assets/routing-e8757775.js.br"
  },
  "/_build/assets/routing-e8757775.js.gz": {
    "type": "application/javascript",
    "encoding": "gzip",
    "etag": "\"2d4c-JYSLlqmXSy1T305iz6MAehFwIAA\"",
    "mtime": "2024-01-08T00:18:01.896Z",
    "size": 11596,
    "path": "../../.output/public/_build/assets/routing-e8757775.js.gz"
  }
};

function readAsset (id) {
  const serverDir = dirname(fileURLToPath(globalThis._importMeta_.url));
  return promises.readFile(resolve(serverDir, assets[id].path))
}

const publicAssetBases = {};

function isPublicAssetURL(id = '') {
  if (assets[id]) {
    return true
  }
  for (const base in publicAssetBases) {
    if (id.startsWith(base)) { return true }
  }
  return false
}

function getAsset (id) {
  return assets[id]
}

const METHODS = /* @__PURE__ */ new Set(["HEAD", "GET"]);
const EncodingMap = { gzip: ".gz", br: ".br" };
const _f4b49z = eventHandler((event) => {
  if (event.method && !METHODS.has(event.method)) {
    return;
  }
  let id = decodePath(
    withLeadingSlash(withoutTrailingSlash(parseURL(event.path).pathname))
  );
  let asset;
  const encodingHeader = String(
    getRequestHeader(event, "accept-encoding") || ""
  );
  const encodings = [
    ...encodingHeader.split(",").map((e) => EncodingMap[e.trim()]).filter(Boolean).sort(),
    ""
  ];
  if (encodings.length > 1) {
    setResponseHeader(event, "Vary", "Accept-Encoding");
  }
  for (const encoding of encodings) {
    for (const _id of [id + encoding, joinURL(id, "index.html" + encoding)]) {
      const _asset = getAsset(_id);
      if (_asset) {
        asset = _asset;
        id = _id;
        break;
      }
    }
  }
  if (!asset) {
    if (isPublicAssetURL(id)) {
      removeResponseHeader(event, "Cache-Control");
      throw createError({
        statusMessage: "Cannot find static asset " + id,
        statusCode: 404
      });
    }
    return;
  }
  const ifNotMatch = getRequestHeader(event, "if-none-match") === asset.etag;
  if (ifNotMatch) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  const ifModifiedSinceH = getRequestHeader(event, "if-modified-since");
  const mtimeDate = new Date(asset.mtime);
  if (ifModifiedSinceH && asset.mtime && new Date(ifModifiedSinceH) >= mtimeDate) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  if (asset.type && !getResponseHeader(event, "Content-Type")) {
    setResponseHeader(event, "Content-Type", asset.type);
  }
  if (asset.etag && !getResponseHeader(event, "ETag")) {
    setResponseHeader(event, "ETag", asset.etag);
  }
  if (asset.mtime && !getResponseHeader(event, "Last-Modified")) {
    setResponseHeader(event, "Last-Modified", mtimeDate.toUTCString());
  }
  if (asset.encoding && !getResponseHeader(event, "Content-Encoding")) {
    setResponseHeader(event, "Content-Encoding", asset.encoding);
  }
  if (asset.size > 0 && !getResponseHeader(event, "Content-Length")) {
    setResponseHeader(event, "Content-Length", asset.size);
  }
  return readAsset(id);
});

var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};
var Ee = ((t) => (t[t.AggregateError = 1] = "AggregateError", t[t.ArrowFunction = 2] = "ArrowFunction", t[t.ErrorPrototypeStack = 4] = "ErrorPrototypeStack", t[t.ObjectAssign = 8] = "ObjectAssign", t[t.BigIntTypedArray = 16] = "BigIntTypedArray", t))(Ee || {});
function h$1(t, e) {
  if (!t)
    throw e;
}
function Ie(t) {
  switch (t) {
    case '"':
      return '\\"';
    case "\\":
      return "\\\\";
    case `
`:
      return "\\n";
    case "\r":
      return "\\r";
    case "\b":
      return "\\b";
    case "	":
      return "\\t";
    case "\f":
      return "\\f";
    case "<":
      return "\\x3C";
    case "\u2028":
      return "\\u2028";
    case "\u2029":
      return "\\u2029";
    default:
      return;
  }
}
function f$1(t) {
  let e = "", r = 0, i;
  for (let s = 0, a = t.length; s < a; s++)
    i = Ie(t[s]), i && (e += t.slice(r, s) + i, r = s + 1);
  return r === 0 ? e = t : e += t.slice(r), e;
}
function Ae(t) {
  switch (t) {
    case "\\\\":
      return "\\";
    case '\\"':
      return '"';
    case "\\n":
      return `
`;
    case "\\r":
      return "\r";
    case "\\b":
      return "\b";
    case "\\t":
      return "	";
    case "\\f":
      return "\f";
    case "\\x3C":
      return "<";
    case "\\u2028":
      return "\u2028";
    case "\\u2029":
      return "\u2029";
    default:
      return t;
  }
}
function v(t) {
  return t.replace(/(\\\\|\\"|\\n|\\r|\\b|\\t|\\f|\\u2028|\\u2029|\\x3C)/g, Ae);
}
var m$1 = "__SEROVAL_REFS__", I = "$R", E = `self.${I}`;
function Re(t) {
  return t == null ? `${E}=${E}||[]` : `(${E}=${E}||{})["${f$1(t)}"]=[]`;
}
var Q$1 = /* @__PURE__ */ new Map(), g$1 = /* @__PURE__ */ new Map();
function j(t) {
  return Q$1.has(t);
}
function xe(t) {
  return g$1.has(t);
}
function Pe(t) {
  return h$1(j(t), new Error("Missing reference id")), Q$1.get(t);
}
function ke(t) {
  return h$1(xe(t), new Error("Missing reference for id:" + t)), g$1.get(t);
}
typeof globalThis < "u" ? Object.defineProperty(globalThis, m$1, { value: g$1, configurable: true, writable: false, enumerable: false }) : typeof self < "u" ? Object.defineProperty(self, m$1, { value: g$1, configurable: true, writable: false, enumerable: false }) : typeof global < "u" && Object.defineProperty(global, m$1, { value: g$1, configurable: true, writable: false, enumerable: false });
function X$1(t, e) {
  for (let r = 0, i = e.length; r < i; r++) {
    let s = e[r];
    t.has(s) || (t.add(s), s.extends && X$1(t, s.extends));
  }
}
function Y$1(t) {
  if (t) {
    let e = /* @__PURE__ */ new Set();
    return X$1(e, t), [...e];
  }
}
var { toString: Fe } = Object.prototype, _ = class extends Error {
  constructor(e) {
    super('Unsupported type "' + Fe.call(e) + '"'), this.value = e;
  }
}, Ve = { 0: "Symbol.asyncIterator", 1: "Symbol.hasInstance", 2: "Symbol.isConcatSpreadable", 3: "Symbol.iterator", 4: "Symbol.match", 5: "Symbol.matchAll", 6: "Symbol.replace", 7: "Symbol.search", 8: "Symbol.species", 9: "Symbol.split", 10: "Symbol.toPrimitive", 11: "Symbol.toStringTag", 12: "Symbol.unscopables" }, C = { [Symbol.asyncIterator]: 0, [Symbol.hasInstance]: 1, [Symbol.isConcatSpreadable]: 2, [Symbol.iterator]: 3, [Symbol.match]: 4, [Symbol.matchAll]: 5, [Symbol.replace]: 6, [Symbol.search]: 7, [Symbol.species]: 8, [Symbol.split]: 9, [Symbol.toPrimitive]: 10, [Symbol.toStringTag]: 11, [Symbol.unscopables]: 12 }, Oe = { 0: Symbol.asyncIterator, 1: Symbol.hasInstance, 2: Symbol.isConcatSpreadable, 3: Symbol.iterator, 4: Symbol.match, 5: Symbol.matchAll, 6: Symbol.replace, 7: Symbol.search, 8: Symbol.species, 9: Symbol.split, 10: Symbol.toPrimitive, 11: Symbol.toStringTag, 12: Symbol.unscopables }, je = { 2: "!0", 3: "!1", 1: "void 0", 0: "null", 4: "-0", 5: "1/0", 6: "-1/0", 7: "0/0" }, Ce = { 2: true, 3: false, 1: void 0, 0: null, 4: -0, 5: 1 / 0, 6: -1 / 0, 7: NaN }, ee$1 = { 0: "Error", 1: "EvalError", 2: "RangeError", 3: "ReferenceError", 4: "SyntaxError", 5: "TypeError", 6: "URIError" }, De = { 0: Error, 1: EvalError, 2: RangeError, 3: ReferenceError, 4: SyntaxError, 5: TypeError, 6: URIError };
function p(t) {
  return { t: 2, i: void 0, s: t, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
var D = p(2), M = p(3), Me = p(1), Te = p(0), $e = p(4), Ue = p(5), Be = p(6), _e = p(7);
function U$1(t) {
  return t instanceof EvalError ? 1 : t instanceof RangeError ? 2 : t instanceof ReferenceError ? 3 : t instanceof SyntaxError ? 4 : t instanceof TypeError ? 5 : t instanceof URIError ? 6 : 0;
}
function We(t) {
  let e = ee$1[U$1(t)];
  return t.name !== e ? { name: t.name } : t.constructor.name !== e ? { name: t.constructor.name } : {};
}
function W$1(t, e) {
  let r = We(t), i = Object.getOwnPropertyNames(t);
  for (let s = 0, a = i.length, n; s < a; s++)
    n = i[s], n !== "name" && n !== "message" && (n === "stack" ? e & 4 && (r = r || {}, r[n] = t[n]) : (r = r || {}, r[n] = t[n]));
  return r;
}
function te$1(t) {
  return Object.isFrozen(t) ? 3 : Object.isSealed(t) ? 2 : Object.isExtensible(t) ? 0 : 1;
}
function Ne(t) {
  switch (t) {
    case 1 / 0:
      return Ue;
    case -1 / 0:
      return Be;
  }
  return t !== t ? _e : Object.is(t, -0) ? $e : { t: 0, i: void 0, s: t, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function T$1(t) {
  return { t: 1, i: void 0, s: f$1(t), l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function Le(t) {
  return { t: 3, i: void 0, s: "" + t, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function qe(t) {
  return { t: 4, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function Ke(t, e) {
  return { t: 5, i: t, s: e.toISOString(), l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, f: void 0, a: void 0, b: void 0, o: void 0 };
}
function He(t, e) {
  return { t: 6, i: t, s: void 0, l: void 0, c: f$1(e.source), m: e.flags, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function Ze(t, e) {
  let r = new Uint8Array(e), i = r.length, s = new Array(i);
  for (let a = 0; a < i; a++)
    s[a] = r[a];
  return { t: 19, i: t, s, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function Je(t, e) {
  return h$1(e in C, new Error("Only well-known symbols are supported.")), { t: 17, i: t, s: C[e], l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function N(t, e) {
  return { t: 18, i: t, s: f$1(Pe(e)), l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function re$1(t, e, r) {
  return { t: 25, i: t, s: r, l: void 0, c: f$1(e), m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function Ge(t, e, r) {
  return { t: 9, i: t, s: void 0, l: e.length, c: void 0, m: void 0, p: void 0, e: void 0, a: r, f: void 0, b: void 0, o: te$1(e) };
}
function Qe(t, e) {
  return { t: 21, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: e, b: void 0, o: void 0 };
}
function Xe(t, e, r) {
  return { t: 15, i: t, s: void 0, l: e.length, c: e.constructor.name, m: void 0, p: void 0, e: void 0, a: void 0, f: r, b: e.byteOffset, o: void 0 };
}
function Ye(t, e, r) {
  return { t: 16, i: t, s: void 0, l: e.length, c: e.constructor.name, m: void 0, p: void 0, e: void 0, a: void 0, f: r, b: e.byteOffset, o: void 0 };
}
function et(t, e, r) {
  return { t: 20, i: t, s: void 0, l: e.byteLength, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: r, b: e.byteOffset, o: void 0 };
}
function tt(t, e, r) {
  return { t: 13, i: t, s: U$1(e), l: void 0, c: void 0, m: f$1(e.message), p: r, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function rt(t, e, r) {
  return { t: 14, i: t, s: U$1(e), l: void 0, c: void 0, m: f$1(e.message), p: r, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
}
function it(t, e, r) {
  return { t: 7, i: t, s: void 0, l: e, c: void 0, m: void 0, p: void 0, e: void 0, a: r, f: void 0, b: void 0, o: void 0 };
}
function ie(t, e) {
  return { t: 28, i: void 0, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: [t, e], f: void 0, b: void 0, o: void 0 };
}
function se$1(t, e) {
  return { t: 30, i: void 0, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: [t, e], f: void 0, b: void 0, o: void 0 };
}
function ae$1(t, e, r) {
  return { t: 31, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: r, f: e, b: void 0, o: void 0 };
}
function st(t, e) {
  return { t: 32, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: e, b: void 0, o: void 0 };
}
function at(t, e) {
  return { t: 33, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: e, b: void 0, o: void 0 };
}
function nt(t, e) {
  return { t: 34, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: e, b: void 0, o: void 0 };
}
function ne$1(t) {
  let e = [], r = -1, i = -1, s = t[Symbol.iterator]();
  for (; ; )
    try {
      let a = s.next();
      if (e.push(a.value), a.done) {
        i = e.length - 1;
        break;
      }
    } catch (a) {
      r = e.length, e.push(a);
    }
  return { v: e, t: r, d: i };
}
function ot(t) {
  return () => {
    let e = 0;
    return { [Symbol.iterator]() {
      return this;
    }, next() {
      if (e > t.d)
        return { done: true, value: void 0 };
      let r = e++, i = t.v[r];
      if (r === t.t)
        throw i;
      return { done: r === t.d, value: i };
    } };
  };
}
var lt = {}, ut = {}, ct = { 0: {}, 1: {}, 2: {}, 3: {}, 4: {} }, dt = class {
  constructor(e) {
    this.marked = /* @__PURE__ */ new Set(), this.plugins = e.plugins, this.features = 31 ^ (e.disabledFeatures || 0), this.refs = e.refs || /* @__PURE__ */ new Map();
  }
  markRef(e) {
    this.marked.add(e);
  }
  isMarked(e) {
    return this.marked.has(e);
  }
  getIndexedValue(e) {
    let r = this.refs.get(e);
    if (r != null)
      return this.markRef(r), { type: 1, value: qe(r) };
    let i = this.refs.size;
    return this.refs.set(e, i), { type: 0, value: i };
  }
  getReference(e) {
    let r = this.getIndexedValue(e);
    return r.type === 1 ? r : j(e) ? { type: 2, value: N(r.value, e) } : r;
  }
  getStrictReference(e) {
    h$1(j(e), new Error("Cannot serialize " + typeof e + " without reference ID."));
    let r = this.getIndexedValue(e);
    return r.type === 1 ? r.value : N(r.value, e);
  }
  parseFunction(e) {
    return this.getStrictReference(e);
  }
  parseWellKnownSymbol(e) {
    let r = this.getReference(e);
    return r.type !== 0 ? r.value : (h$1(e in C, new Error("Cannot serialized unsupported symbol.")), Je(r.value, e));
  }
  parseSpecialReference(e) {
    let r = this.getIndexedValue(ct[e]);
    return r.type === 1 ? r.value : { t: 26, i: r.value, s: e, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: void 0, b: void 0, o: void 0 };
  }
  parseIteratorFactory() {
    let e = this.getIndexedValue(lt);
    return e.type === 1 ? e.value : { t: 27, i: e.value, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: this.parseWellKnownSymbol(Symbol.iterator), b: void 0, o: void 0 };
  }
  parseAsyncIteratorFactory() {
    let e = this.getIndexedValue(ut);
    return e.type === 1 ? e.value : { t: 29, i: e.value, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: [this.parseSpecialReference(1), this.parseWellKnownSymbol(Symbol.asyncIterator)], f: void 0, b: void 0, o: void 0 };
  }
  createObjectNode(e, r, i, s) {
    return { t: i ? 11 : 10, i: e, s: void 0, l: void 0, c: void 0, m: void 0, p: s, e: void 0, a: void 0, f: void 0, b: void 0, o: te$1(r) };
  }
  createMapNode(e, r, i, s) {
    return { t: 8, i: e, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: { k: r, v: i, s }, a: void 0, f: this.parseSpecialReference(0), b: void 0, o: void 0 };
  }
  createPromiseConstructorNode(e) {
    return { t: 22, i: e, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: void 0, f: this.parseSpecialReference(1), b: void 0, o: void 0 };
  }
};
function $$1() {
  let t, e;
  return { promise: new Promise((r, i) => {
    t = r, e = i;
  }), resolve(r) {
    t(r);
  }, reject(r) {
    e(r);
  } };
}
function ht(t) {
  return "__SEROVAL_STREAM__" in t;
}
function w$1() {
  let t = /* @__PURE__ */ new Set(), e = [], r = true, i = false;
  function s(o) {
    for (let l of t.keys())
      l.next(o);
  }
  function a(o) {
    for (let l of t.keys())
      l.throw(o);
  }
  function n(o) {
    for (let l of t.keys())
      l.return(o);
  }
  return { __SEROVAL_STREAM__: true, on(o) {
    r && t.add(o);
    for (let l = 0, u = e.length; l < u; l++) {
      let d = e[l];
      l === u - 1 ? i ? o.return(d) : o.throw(d) : o.next(d);
    }
    return () => {
      r && t.delete(o);
    };
  }, next(o) {
    r && (e.push(o), s(o));
  }, throw(o) {
    r && (e.push(o), a(o), r = false, i = false, t.clear());
  }, return(o) {
    r && (e.push(o), n(o), r = false, i = true, t.clear());
  } };
}
function ft(t) {
  let e = w$1(), r = t[Symbol.asyncIterator]();
  async function i() {
    try {
      let s = await r.next();
      s.done ? e.return(s.value) : (e.next(s.value), await i());
    } catch (s) {
      e.throw(s);
    }
  }
  return i().catch(() => {
  }), e;
}
function pt(t) {
  return () => {
    let e = [], r = [], i = 0, s = -1, a = false;
    function n() {
      for (let l = 0, u = r.length; l < u; l++)
        r[l].resolve({ done: true, value: void 0 });
    }
    t.on({ next(l) {
      let u = r.shift();
      u && u.resolve({ done: false, value: l }), e.push(l);
    }, throw(l) {
      let u = r.shift();
      u && u.reject(l), n(), s = e.length, e.push(l), a = true;
    }, return(l) {
      let u = r.shift();
      u && u.resolve({ done: true, value: l }), n(), s = e.length, e.push(l);
    } });
    function o() {
      let l = i++, u = e[l];
      if (l !== s)
        return { done: false, value: u };
      if (a)
        throw u;
      return { done: true, value: u };
    }
    return { [Symbol.asyncIterator]() {
      return this;
    }, async next() {
      if (s === -1) {
        let l = i++;
        if (l >= e.length) {
          let u = $$1();
          return r.push(u), await u.promise;
        }
        return { done: false, value: e[l] };
      }
      return i > s ? { done: true, value: void 0 } : o();
    } };
  };
}
function vt(t) {
  switch (t) {
    case "Int8Array":
      return Int8Array;
    case "Int16Array":
      return Int16Array;
    case "Int32Array":
      return Int32Array;
    case "Uint8Array":
      return Uint8Array;
    case "Uint16Array":
      return Uint16Array;
    case "Uint32Array":
      return Uint32Array;
    case "Uint8ClampedArray":
      return Uint8ClampedArray;
    case "Float32Array":
      return Float32Array;
    case "Float64Array":
      return Float64Array;
    case "BigInt64Array":
      return BigInt64Array;
    case "BigUint64Array":
      return BigUint64Array;
    default:
      throw new Error(`Unknown TypedArray "${t}"`);
  }
}
function L(t, e) {
  switch (e) {
    case 3:
      return Object.freeze(t);
    case 1:
      return Object.preventExtensions(t);
    case 2:
      return Object.seal(t);
    default:
      return t;
  }
}
var gt = class {
  constructor(e) {
    this.plugins = e.plugins, this.refs = e.refs || /* @__PURE__ */ new Map();
  }
  deserializeReference(e) {
    return this.assignIndexedValue(e.i, ke(v(e.s)));
  }
  deserializeArray(e) {
    let r = e.l, i = this.assignIndexedValue(e.i, new Array(r)), s;
    for (let a = 0; a < r; a++)
      s = e.a[a], s && (i[a] = this.deserialize(s));
    return L(i, e.o), i;
  }
  deserializeProperties(e, r) {
    let i = e.s;
    if (i) {
      let s = e.k, a = e.v;
      for (let n = 0, o; n < i; n++)
        o = s[n], typeof o == "string" ? r[v(o)] = this.deserialize(a[n]) : r[this.deserialize(o)] = this.deserialize(a[n]);
    }
    return r;
  }
  deserializeObject(e) {
    let r = this.assignIndexedValue(e.i, e.t === 10 ? {} : /* @__PURE__ */ Object.create(null));
    return this.deserializeProperties(e.p, r), L(r, e.o), r;
  }
  deserializeDate(e) {
    return this.assignIndexedValue(e.i, new Date(e.s));
  }
  deserializeRegExp(e) {
    return this.assignIndexedValue(e.i, new RegExp(v(e.c), e.m));
  }
  deserializeSet(e) {
    let r = this.assignIndexedValue(e.i, /* @__PURE__ */ new Set()), i = e.a;
    for (let s = 0, a = e.l; s < a; s++)
      r.add(this.deserialize(i[s]));
    return r;
  }
  deserializeMap(e) {
    let r = this.assignIndexedValue(e.i, /* @__PURE__ */ new Map()), i = e.e.k, s = e.e.v;
    for (let a = 0, n = e.e.s; a < n; a++)
      r.set(this.deserialize(i[a]), this.deserialize(s[a]));
    return r;
  }
  deserializeArrayBuffer(e) {
    let r = new Uint8Array(e.s);
    return this.assignIndexedValue(e.i, r.buffer);
  }
  deserializeTypedArray(e) {
    let r = vt(e.c), i = this.deserialize(e.f);
    return this.assignIndexedValue(e.i, new r(i, e.b, e.l));
  }
  deserializeDataView(e) {
    let r = this.deserialize(e.f);
    return this.assignIndexedValue(e.i, new DataView(r, e.b, e.l));
  }
  deserializeDictionary(e, r) {
    if (e.p) {
      let i = this.deserializeProperties(e.p, {});
      Object.assign(r, i);
    }
    return r;
  }
  deserializeAggregateError(e) {
    let r = this.assignIndexedValue(e.i, new AggregateError([], v(e.m)));
    return this.deserializeDictionary(e, r);
  }
  deserializeError(e) {
    let r = De[e.s], i = this.assignIndexedValue(e.i, new r(v(e.m)));
    return this.deserializeDictionary(e, i);
  }
  deserializePromise(e) {
    let r = $$1(), i = this.assignIndexedValue(e.i, r), s = this.deserialize(e.f);
    return e.s ? r.resolve(s) : r.reject(s), i.promise;
  }
  deserializeBoxed(e) {
    return this.assignIndexedValue(e.i, Object(this.deserialize(e.f)));
  }
  deserializePlugin(e) {
    let r = this.plugins;
    if (r) {
      let i = v(e.c);
      for (let s = 0, a = r.length; s < a; s++) {
        let n = r[s];
        if (n.tag === i)
          return this.assignIndexedValue(e.i, n.deserialize(e.s, this, { id: e.i }));
      }
    }
    throw new Error('Missing plugin for tag "' + e.c + '".');
  }
  deserializePromiseConstructor(e) {
    return this.assignIndexedValue(e.i, $$1()).promise;
  }
  deserializePromiseResolve(e) {
    let r = this.refs.get(e.i);
    h$1(r, new Error("Missing Promise instance.")), r.resolve(this.deserialize(e.a[1]));
  }
  deserializePromiseReject(e) {
    let r = this.refs.get(e.i);
    h$1(r, new Error("Missing Promise instance.")), r.reject(this.deserialize(e.a[1]));
  }
  deserializeIteratorFactoryInstance(e) {
    this.deserialize(e.a[0]);
    let r = this.deserialize(e.a[1]);
    return ot(r);
  }
  deserializeAsyncIteratorFactoryInstance(e) {
    this.deserialize(e.a[0]);
    let r = this.deserialize(e.a[1]);
    return pt(r);
  }
  deserializeStreamConstructor(e) {
    let r = this.assignIndexedValue(e.i, w$1()), i = e.a.length;
    if (i)
      for (let s = 0; s < i; s++)
        this.deserialize(e.a[s]);
    return r;
  }
  deserializeStreamNext(e) {
    let r = this.refs.get(e.i);
    h$1(r, new Error("Missing Stream instance.")), r.next(this.deserialize(e.f));
  }
  deserializeStreamThrow(e) {
    let r = this.refs.get(e.i);
    h$1(r, new Error("Missing Stream instance.")), r.throw(this.deserialize(e.f));
  }
  deserializeStreamReturn(e) {
    let r = this.refs.get(e.i);
    h$1(r, new Error("Missing Stream instance.")), r.return(this.deserialize(e.f));
  }
  deserializeIteratorFactory(e) {
    this.deserialize(e.f);
  }
  deserializeAsyncIteratorFactory(e) {
    this.deserialize(e.a[1]);
  }
  deserialize(e) {
    switch (e.t) {
      case 2:
        return Ce[e.s];
      case 0:
        return e.s;
      case 1:
        return v(e.s);
      case 3:
        return BigInt(e.s);
      case 4:
        return this.refs.get(e.i);
      case 18:
        return this.deserializeReference(e);
      case 9:
        return this.deserializeArray(e);
      case 10:
      case 11:
        return this.deserializeObject(e);
      case 5:
        return this.deserializeDate(e);
      case 6:
        return this.deserializeRegExp(e);
      case 7:
        return this.deserializeSet(e);
      case 8:
        return this.deserializeMap(e);
      case 19:
        return this.deserializeArrayBuffer(e);
      case 16:
      case 15:
        return this.deserializeTypedArray(e);
      case 20:
        return this.deserializeDataView(e);
      case 14:
        return this.deserializeAggregateError(e);
      case 13:
        return this.deserializeError(e);
      case 12:
        return this.deserializePromise(e);
      case 17:
        return Oe[e.s];
      case 21:
        return this.deserializeBoxed(e);
      case 25:
        return this.deserializePlugin(e);
      case 22:
        return this.deserializePromiseConstructor(e);
      case 23:
        return this.deserializePromiseResolve(e);
      case 24:
        return this.deserializePromiseReject(e);
      case 28:
        return this.deserializeIteratorFactoryInstance(e);
      case 30:
        return this.deserializeAsyncIteratorFactoryInstance(e);
      case 31:
        return this.deserializeStreamConstructor(e);
      case 32:
        return this.deserializeStreamNext(e);
      case 33:
        return this.deserializeStreamThrow(e);
      case 34:
        return this.deserializeStreamReturn(e);
      case 27:
        return this.deserializeIteratorFactory(e);
      case 29:
        return this.deserializeAsyncIteratorFactory(e);
      default:
        throw new Error("invariant");
    }
  }
}, mt = class extends gt {
  constructor(t) {
    super(t), this.mode = "vanilla", this.marked = new Set(t.markedRefs);
  }
  assignIndexedValue(t, e) {
    return this.marked.has(t) && this.refs.set(t, e), e;
  }
}, yt = /^[$A-Z_][0-9A-Z_$]*$/i;
function q(t) {
  let e = t[0];
  return (e === "$" || e === "_" || e >= "A" && e <= "Z" || e >= "a" && e <= "z") && yt.test(t);
}
function y(t) {
  switch (t.t) {
    case 0:
      return t.s + "=" + t.v;
    case 2:
      return t.s + ".set(" + t.k + "," + t.v + ")";
    case 1:
      return t.s + ".add(" + t.v + ")";
    case 3:
      return t.s + ".delete(" + t.k + ")";
  }
}
function bt(t) {
  let e = [], r = t[0];
  for (let i = 1, s = t.length, a, n = r; i < s; i++)
    a = t[i], a.t === 0 && a.v === n.v ? r = { t: 0, s: a.s, k: void 0, v: y(r) } : a.t === 2 && a.s === n.s ? r = { t: 2, s: y(r), k: a.k, v: a.v } : a.t === 1 && a.s === n.s ? r = { t: 1, s: y(r), k: void 0, v: a.v } : a.t === 3 && a.s === n.s ? r = { t: 3, s: y(r), k: a.k, v: void 0 } : (e.push(r), r = a), n = a;
  return e.push(r), e;
}
function K(t) {
  if (t.length) {
    let e = "", r = bt(t);
    for (let i = 0, s = r.length; i < s; i++)
      e += y(r[i]) + ",";
    return e;
  }
}
var zt = "Object.create(null)", wt = "new Set", St = "new Map", Et = "Promise.resolve", It = "Promise.reject", At = { 3: "Object.freeze", 2: "Object.seal", 1: "Object.preventExtensions", 0: void 0 }, Rt = class {
  constructor(t) {
    this.stack = [], this.flags = [], this.assignments = [], this.plugins = t.plugins, this.features = t.features, this.marked = new Set(t.markedRefs);
  }
  createFunction(t, e) {
    return this.features & 2 ? (t.length === 1 ? t[0] : "(" + t.join(",") + ")") + "=>" + e : "function(" + t.join(",") + "){return " + e + "}";
  }
  createEffectfulFunction(t, e) {
    return this.features & 2 ? (t.length === 1 ? t[0] : "(" + t.join(",") + ")") + "=>{" + e + "}" : "function(" + t.join(",") + "){" + e + "}";
  }
  markRef(t) {
    this.marked.add(t);
  }
  isMarked(t) {
    return this.marked.has(t);
  }
  pushObjectFlag(t, e) {
    t !== 0 && (this.markRef(e), this.flags.push({ type: t, value: this.getRefParam(e) }));
  }
  resolveFlags() {
    let t = "";
    for (let e = 0, r = this.flags, i = r.length; e < i; e++) {
      let s = r[e];
      t += At[s.type] + "(" + s.value + "),";
    }
    return t;
  }
  resolvePatches() {
    let t = K(this.assignments), e = this.resolveFlags();
    return t ? e ? t + e : t : e;
  }
  createAssignment(t, e) {
    this.assignments.push({ t: 0, s: t, k: void 0, v: e });
  }
  createAddAssignment(t, e) {
    this.assignments.push({ t: 1, s: this.getRefParam(t), k: void 0, v: e });
  }
  createSetAssignment(t, e, r) {
    this.assignments.push({ t: 2, s: this.getRefParam(t), k: e, v: r });
  }
  createDeleteAssignment(t, e) {
    this.assignments.push({ t: 3, s: this.getRefParam(t), k: e, v: void 0 });
  }
  createArrayAssign(t, e, r) {
    this.createAssignment(this.getRefParam(t) + "[" + e + "]", r);
  }
  createObjectAssign(t, e, r) {
    this.createAssignment(this.getRefParam(t) + "." + e, r);
  }
  isIndexedValueInStack(t) {
    return t.t === 4 && this.stack.includes(t.i);
  }
  serializeReference(t) {
    return this.assignIndexedValue(t.i, m$1 + '.get("' + t.s + '")');
  }
  serializeArrayItem(t, e, r) {
    return e ? this.isIndexedValueInStack(e) ? (this.markRef(t), this.createArrayAssign(t, r, this.getRefParam(e.i)), "") : this.serialize(e) : "";
  }
  serializeArray(t) {
    let e = t.i;
    if (t.l) {
      this.stack.push(e);
      let r = t.a, i = this.serializeArrayItem(e, r[0], 0), s = i === "";
      for (let a = 1, n = t.l, o; a < n; a++)
        o = this.serializeArrayItem(e, r[a], a), i += "," + o, s = o === "";
      return this.stack.pop(), this.pushObjectFlag(t.o, t.i), this.assignIndexedValue(e, "[" + i + (s ? ",]" : "]"));
    }
    return this.assignIndexedValue(e, "[]");
  }
  serializeProperty(t, e, r) {
    if (typeof e == "string") {
      let i = Number(e), s = i >= 0 && i.toString() === e || q(e);
      if (this.isIndexedValueInStack(r)) {
        let a = this.getRefParam(r.i);
        return this.markRef(t.i), s && i !== i ? this.createObjectAssign(t.i, e, a) : this.createArrayAssign(t.i, s ? e : '"' + e + '"', a), "";
      }
      return (s ? e : '"' + e + '"') + ":" + this.serialize(r);
    }
    return "[" + this.serialize(e) + "]:" + this.serialize(r);
  }
  serializeProperties(t, e) {
    let r = e.s;
    if (r) {
      let i = e.k, s = e.v;
      this.stack.push(t.i);
      let a = this.serializeProperty(t, i[0], s[0]);
      for (let n = 1, o = a; n < r; n++)
        o = this.serializeProperty(t, i[n], s[n]), a += (o && a && ",") + o;
      return this.stack.pop(), "{" + a + "}";
    }
    return "{}";
  }
  serializeObject(t) {
    return this.pushObjectFlag(t.o, t.i), this.assignIndexedValue(t.i, this.serializeProperties(t, t.p));
  }
  serializeWithObjectAssign(t, e, r) {
    let i = this.serializeProperties(t, e);
    return i !== "{}" ? "Object.assign(" + r + "," + i + ")" : r;
  }
  serializeStringKeyAssignment(t, e, r, i) {
    let s = this.serialize(i), a = Number(r), n = a >= 0 && a.toString() === r || q(r);
    if (this.isIndexedValueInStack(i))
      n && a !== a ? this.createObjectAssign(t.i, r, s) : this.createArrayAssign(t.i, n ? r : '"' + r + '"', s);
    else {
      let o = this.assignments;
      this.assignments = e, n && a !== a ? this.createObjectAssign(t.i, r, s) : this.createArrayAssign(t.i, n ? r : '"' + r + '"', s), this.assignments = o;
    }
  }
  serializeAssignment(t, e, r, i) {
    if (typeof r == "string")
      this.serializeStringKeyAssignment(t, e, r, i);
    else {
      let s = this.stack;
      this.stack = [];
      let a = this.serialize(i);
      this.stack = s;
      let n = this.assignments;
      this.assignments = e, this.createArrayAssign(t.i, this.serialize(r), a), this.assignments = n;
    }
  }
  serializeAssignments(t, e) {
    let r = e.s;
    if (r) {
      let i = [], s = e.k, a = e.v;
      this.stack.push(t.i);
      for (let n = 0; n < r; n++)
        this.serializeAssignment(t, i, s[n], a[n]);
      return this.stack.pop(), K(i);
    }
  }
  serializeDictionary(t, e) {
    if (t.p)
      if (this.features & 8)
        e = this.serializeWithObjectAssign(t, t.p, e);
      else {
        this.markRef(t.i);
        let r = this.serializeAssignments(t, t.p);
        if (r)
          return "(" + this.assignIndexedValue(t.i, e) + "," + r + this.getRefParam(t.i) + ")";
      }
    return this.assignIndexedValue(t.i, e);
  }
  serializeNullConstructor(t) {
    return this.pushObjectFlag(t.o, t.i), this.serializeDictionary(t, zt);
  }
  serializeDate(t) {
    return this.assignIndexedValue(t.i, 'new Date("' + t.s + '")');
  }
  serializeRegExp(t) {
    return this.assignIndexedValue(t.i, "/" + t.c + "/" + t.m);
  }
  serializeSetItem(t, e) {
    return this.isIndexedValueInStack(e) ? (this.markRef(t), this.createAddAssignment(t, this.getRefParam(e.i)), "") : this.serialize(e);
  }
  serializeSet(t) {
    let e = wt, r = t.l, i = t.i;
    if (r) {
      let s = t.a;
      this.stack.push(i);
      let a = this.serializeSetItem(i, s[0]);
      for (let n = 1, o = a; n < r; n++)
        o = this.serializeSetItem(i, s[n]), a += (o && a && ",") + o;
      this.stack.pop(), a && (e += "([" + a + "])");
    }
    return this.assignIndexedValue(i, e);
  }
  serializeMapEntry(t, e, r, i) {
    if (this.isIndexedValueInStack(e)) {
      let s = this.getRefParam(e.i);
      if (this.markRef(t), this.isIndexedValueInStack(r)) {
        let n = this.getRefParam(r.i);
        return this.createSetAssignment(t, s, n), "";
      }
      if (r.t !== 4 && r.i != null && this.isMarked(r.i)) {
        let n = "(" + this.serialize(r) + ",[" + i + "," + i + "])";
        return this.createSetAssignment(t, s, this.getRefParam(r.i)), this.createDeleteAssignment(t, i), n;
      }
      let a = this.stack;
      return this.stack = [], this.createSetAssignment(t, s, this.serialize(r)), this.stack = a, "";
    }
    if (this.isIndexedValueInStack(r)) {
      let s = this.getRefParam(r.i);
      if (this.markRef(t), e.t !== 4 && e.i != null && this.isMarked(e.i)) {
        let n = "(" + this.serialize(e) + ",[" + i + "," + i + "])";
        return this.createSetAssignment(t, this.getRefParam(e.i), s), this.createDeleteAssignment(t, i), n;
      }
      let a = this.stack;
      return this.stack = [], this.createSetAssignment(t, this.serialize(e), s), this.stack = a, "";
    }
    return "[" + this.serialize(e) + "," + this.serialize(r) + "]";
  }
  serializeMap(t) {
    let e = St, r = t.e.s, i = t.i, s = t.f, a = this.getRefParam(s.i);
    if (r) {
      let n = t.e.k, o = t.e.v;
      this.stack.push(i);
      let l = this.serializeMapEntry(i, n[0], o[0], a);
      for (let u = 1, d = l; u < r; u++)
        d = this.serializeMapEntry(i, n[u], o[u], a), l += (d && l && ",") + d;
      this.stack.pop(), l && (e += "([" + l + "])");
    }
    return s.t === 26 && (this.markRef(s.i), e = "(" + this.serialize(s) + "," + e + ")"), this.assignIndexedValue(i, e);
  }
  serializeArrayBuffer(t) {
    let e = "new Uint8Array(", r = t.s, i = r.length;
    if (i) {
      e += "[" + r[0];
      for (let s = 1; s < i; s++)
        e += "," + r[s];
      e += "]";
    }
    return this.assignIndexedValue(t.i, e + ").buffer");
  }
  serializeTypedArray(t) {
    return this.assignIndexedValue(t.i, "new " + t.c + "(" + this.serialize(t.f) + "," + t.b + "," + t.l + ")");
  }
  serializeDataView(t) {
    return this.assignIndexedValue(t.i, "new DataView(" + this.serialize(t.f) + "," + t.b + "," + t.l + ")");
  }
  serializeAggregateError(t) {
    let e = t.i;
    this.stack.push(e);
    let r = this.serializeDictionary(t, 'new AggregateError([],"' + t.m + '")');
    return this.stack.pop(), r;
  }
  serializeError(t) {
    return this.serializeDictionary(t, "new " + ee$1[t.s] + '("' + t.m + '")');
  }
  serializePromise(t) {
    let e, r = t.f, i = t.i, s = t.s ? Et : It;
    if (this.isIndexedValueInStack(r)) {
      let a = this.getRefParam(r.i);
      e = s + (t.s ? "().then(" + this.createFunction([], a) + ")" : "().catch(" + this.createEffectfulFunction([], "throw " + a) + ")");
    } else {
      this.stack.push(i);
      let a = this.serialize(r);
      this.stack.pop(), e = s + "(" + a + ")";
    }
    return this.assignIndexedValue(i, e);
  }
  serializeWellKnownSymbol(t) {
    return this.assignIndexedValue(t.i, Ve[t.s]);
  }
  serializeBoxed(t) {
    return this.assignIndexedValue(t.i, "Object(" + this.serialize(t.f) + ")");
  }
  serializePlugin(t) {
    let e = this.plugins;
    if (e)
      for (let r = 0, i = e.length; r < i; r++) {
        let s = e[r];
        if (s.tag === t.c)
          return this.assignIndexedValue(t.i, s.serialize(t.s, this, { id: t.i }));
      }
    throw new Error('Missing plugin for tag "' + t.c + '".');
  }
  getConstructor(t) {
    let e = this.serialize(t);
    return e === this.getRefParam(t.i) ? e : "(" + e + ")";
  }
  serializePromiseConstructor(t) {
    return this.assignIndexedValue(t.i, this.getConstructor(t.f) + "()");
  }
  serializePromiseResolve(t) {
    return this.getConstructor(t.a[0]) + "(" + this.getRefParam(t.i) + "," + this.serialize(t.a[1]) + ")";
  }
  serializePromiseReject(t) {
    return this.getConstructor(t.a[0]) + "(" + this.getRefParam(t.i) + "," + this.serialize(t.a[1]) + ")";
  }
  serializeSpecialReferenceValue(t) {
    switch (t) {
      case 0:
        return "[]";
      case 1:
        return this.createFunction(["s", "f", "p"], "((p=new Promise(" + this.createEffectfulFunction(["a", "b"], "s=a,f=b") + ")).s=s,p.f=f,p)");
      case 2:
        return this.createEffectfulFunction(["p", "d"], 'p.s(d),p.status="success",p.value=d;delete p.s;delete p.f');
      case 3:
        return this.createEffectfulFunction(["p", "d"], 'p.f(d),p.status="failure",p.value=d;delete p.s;delete p.f');
      case 4:
        return this.createFunction(["b", "a", "s", "l", "p", "f", "e", "n"], "(b=[],a=!0,s=!1,l=[],p=0,f=" + this.createEffectfulFunction(["v", "m", "x"], "for(x=0;x<p;x++)l[x]&&l[x][m](v)") + ",n=" + this.createEffectfulFunction(["o", "x", "z", "c"], 'for(x=0,z=b.length;x<z;x++)(c=b[x],x===z-1?o[s?"return":"throw"](c):o.next(c))') + ",e=" + this.createFunction(["o", "t"], "(a&&(l[t=p++]=o),n(o)," + this.createEffectfulFunction([], "a&&(l[t]=void 0)") + ")") + ",{__SEROVAL_STREAM__:!0,on:" + this.createFunction(["o"], "e(o)") + ",next:" + this.createEffectfulFunction(["v"], 'a&&(b.push(v),f(v,"next"))') + ",throw:" + this.createEffectfulFunction(["v"], 'a&&(b.push(v),f(v,"throw"),a=s=!1,l.length=0)') + ",return:" + this.createEffectfulFunction(["v"], 'a&&(b.push(v),f(v,"return"),a=!1,s=!0,l.length=0)') + "})");
      default:
        return "";
    }
  }
  serializeSpecialReference(t) {
    return this.assignIndexedValue(t.i, this.serializeSpecialReferenceValue(t.s));
  }
  serializeIteratorFactory(t) {
    let e = "", r = false;
    return t.f.t !== 4 && (this.markRef(t.f.i), e = "(" + this.serialize(t.f) + ",", r = true), e += this.assignIndexedValue(t.i, this.createFunction(["s"], this.createFunction(["i", "c", "d", "t"], "(i=0,t={[" + this.getRefParam(t.f.i) + "]:" + this.createFunction([], "t") + ",next:" + this.createEffectfulFunction([], "if(i>s.d)return{done:!0,value:void 0};if(d=s.v[c=i++],c===s.t)throw d;return{done:c===s.d,value:d}") + "})"))), r && (e += ")"), e;
  }
  serializeIteratorFactoryInstance(t) {
    return this.getConstructor(t.a[0]) + "(" + this.serialize(t.a[1]) + ")";
  }
  serializeAsyncIteratorFactory(t) {
    let e = t.a[0], r = t.a[1], i = "";
    e.t !== 4 && (this.markRef(e.i), i += "(" + this.serialize(e)), r.t !== 4 && (this.markRef(r.i), i += (i ? "," : "(") + this.serialize(r)), i && (i += ",");
    let s = this.assignIndexedValue(t.i, this.createFunction(["s"], this.createFunction(["b", "c", "p", "d", "e", "t", "f"], "(b=[],c=0,p=[],d=-1,e=!1,f=" + this.createEffectfulFunction(["i", "l"], "for(i=0,l=p.length;i<l;i++)p[i].s({done:!0,value:void 0})") + ",s.on({next:" + this.createEffectfulFunction(["v", "t"], "if(t=p.shift())t.s({done:!1,value:v});b.push(v)") + ",throw:" + this.createEffectfulFunction(["v", "t"], "if(t=p.shift())t.f(v);f(),d=b.length,e=!0,b.push(v)") + ",return:" + this.createEffectfulFunction(["v", "t"], "if(t=p.shift())t.s({done:!0,value:v});f(),d=b.length,b.push(v)") + "}),t={[" + this.getRefParam(r.i) + "]:" + this.createFunction([], "t") + ",next:" + this.createEffectfulFunction(["i", "t", "v"], "if(d===-1){return((i=c++)>=b.length)?(p.push(t=" + this.getRefParam(e.i) + "()),t):{done:!0,value:b[i]}}if(c>d)return{done:!0,value:void 0};if(v=b[i=c++],i!==d)return{done:!1,value:v};if(e)throw v;return{done:!0,value:v}") + "})")));
    return i ? i + s + ")" : s;
  }
  serializeAsyncIteratorFactoryInstance(t) {
    return this.getConstructor(t.a[0]) + "(" + this.serialize(t.a[1]) + ")";
  }
  serializeStreamConstructor(t) {
    let e = this.assignIndexedValue(t.i, this.getConstructor(t.f) + "()"), r = t.a.length;
    if (r) {
      let i = this.serialize(t.a[0]);
      for (let s = 1; s < r; s++)
        i += "," + this.serialize(t.a[s]);
      return "(" + e + "," + i + "," + this.getRefParam(t.i) + ")";
    }
    return e;
  }
  serializeStreamNext(t) {
    return this.getRefParam(t.i) + ".next(" + this.serialize(t.f) + ")";
  }
  serializeStreamThrow(t) {
    return this.getRefParam(t.i) + ".throw(" + this.serialize(t.f) + ")";
  }
  serializeStreamReturn(t) {
    return this.getRefParam(t.i) + ".return(" + this.serialize(t.f) + ")";
  }
  serialize(t) {
    switch (t.t) {
      case 2:
        return je[t.s];
      case 0:
        return "" + t.s;
      case 1:
        return '"' + t.s + '"';
      case 3:
        return t.s + "n";
      case 4:
        return this.getRefParam(t.i);
      case 18:
        return this.serializeReference(t);
      case 9:
        return this.serializeArray(t);
      case 10:
        return this.serializeObject(t);
      case 11:
        return this.serializeNullConstructor(t);
      case 5:
        return this.serializeDate(t);
      case 6:
        return this.serializeRegExp(t);
      case 7:
        return this.serializeSet(t);
      case 8:
        return this.serializeMap(t);
      case 19:
        return this.serializeArrayBuffer(t);
      case 16:
      case 15:
        return this.serializeTypedArray(t);
      case 20:
        return this.serializeDataView(t);
      case 14:
        return this.serializeAggregateError(t);
      case 13:
        return this.serializeError(t);
      case 12:
        return this.serializePromise(t);
      case 17:
        return this.serializeWellKnownSymbol(t);
      case 21:
        return this.serializeBoxed(t);
      case 22:
        return this.serializePromiseConstructor(t);
      case 23:
        return this.serializePromiseResolve(t);
      case 24:
        return this.serializePromiseReject(t);
      case 25:
        return this.serializePlugin(t);
      case 26:
        return this.serializeSpecialReference(t);
      case 27:
        return this.serializeIteratorFactory(t);
      case 28:
        return this.serializeIteratorFactoryInstance(t);
      case 29:
        return this.serializeAsyncIteratorFactory(t);
      case 30:
        return this.serializeAsyncIteratorFactoryInstance(t);
      case 31:
        return this.serializeStreamConstructor(t);
      case 32:
        return this.serializeStreamNext(t);
      case 33:
        return this.serializeStreamThrow(t);
      case 34:
        return this.serializeStreamReturn(t);
      default:
        throw new Error("invariant");
    }
  }
}, xt = class extends dt {
  parseItems(e) {
    let r = [];
    for (let i = 0, s = e.length; i < s; i++)
      i in e && (r[i] = this.parse(e[i]));
    return r;
  }
  parseArray(e, r) {
    return Ge(e, r, this.parseItems(r));
  }
  parseProperties(e) {
    let r = Object.entries(e), i = [], s = [];
    for (let n = 0, o = r.length; n < o; n++)
      i.push(f$1(r[n][0])), s.push(this.parse(r[n][1]));
    let a = Symbol.iterator;
    return a in e && (i.push(this.parseWellKnownSymbol(a)), s.push(ie(this.parseIteratorFactory(), this.parse(ne$1(e))))), a = Symbol.asyncIterator, a in e && (i.push(this.parseWellKnownSymbol(a)), s.push(se$1(this.parseAsyncIteratorFactory(), this.parse(w$1())))), a = Symbol.toStringTag, a in e && (i.push(this.parseWellKnownSymbol(a)), s.push(T$1(e[a]))), a = Symbol.isConcatSpreadable, a in e && (i.push(this.parseWellKnownSymbol(a)), s.push(e[a] ? D : M)), { k: i, v: s, s: i.length };
  }
  parsePlainObject(e, r, i) {
    return this.createObjectNode(e, r, i, this.parseProperties(r));
  }
  parseBoxed(e, r) {
    return Qe(e, this.parse(r.valueOf()));
  }
  parseTypedArray(e, r) {
    return Xe(e, r, this.parse(r.buffer));
  }
  parseBigIntTypedArray(e, r) {
    return Ye(e, r, this.parse(r.buffer));
  }
  parseDataView(e, r) {
    return et(e, r, this.parse(r.buffer));
  }
  parseError(e, r) {
    let i = W$1(r, this.features);
    return tt(e, r, i ? this.parseProperties(i) : void 0);
  }
  parseAggregateError(e, r) {
    let i = W$1(r, this.features);
    return rt(e, r, i ? this.parseProperties(i) : void 0);
  }
  parseMap(e, r) {
    let i = [], s = [];
    for (let [a, n] of r.entries())
      i.push(this.parse(a)), s.push(this.parse(n));
    return this.createMapNode(e, i, s, r.size);
  }
  parseSet(e, r) {
    let i = [];
    for (let s of r.keys())
      i.push(this.parse(s));
    return it(e, r.size, i);
  }
  parsePlugin(e, r) {
    let i = this.plugins;
    if (i)
      for (let s = 0, a = i.length; s < a; s++) {
        let n = i[s];
        if (n.parse.sync && n.test(r))
          return re$1(e, n.tag, n.parse.sync(r, this, { id: e }));
      }
  }
  parseStream(e, r) {
    return ae$1(e, this.parseSpecialReference(4), []);
  }
  parsePromise(e, r) {
    return this.createPromiseConstructorNode(e);
  }
  parseObject(e, r) {
    if (Array.isArray(r))
      return this.parseArray(e, r);
    if (ht(r))
      return this.parseStream(e, r);
    let i = this.parsePlugin(e, r);
    if (i)
      return i;
    let s = r.constructor;
    switch (s) {
      case Object:
        return this.parsePlainObject(e, r, false);
      case void 0:
        return this.parsePlainObject(e, r, true);
      case Date:
        return Ke(e, r);
      case RegExp:
        return He(e, r);
      case Error:
      case EvalError:
      case RangeError:
      case ReferenceError:
      case SyntaxError:
      case TypeError:
      case URIError:
        return this.parseError(e, r);
      case Number:
      case Boolean:
      case String:
      case BigInt:
        return this.parseBoxed(e, r);
      case ArrayBuffer:
        return Ze(e, r);
      case Int8Array:
      case Int16Array:
      case Int32Array:
      case Uint8Array:
      case Uint16Array:
      case Uint32Array:
      case Uint8ClampedArray:
      case Float32Array:
      case Float64Array:
        return this.parseTypedArray(e, r);
      case DataView:
        return this.parseDataView(e, r);
      case Map:
        return this.parseMap(e, r);
      case Set:
        return this.parseSet(e, r);
    }
    if (s === Promise || r instanceof Promise)
      return this.parsePromise(e, r);
    let a = this.features;
    if (a & 16)
      switch (s) {
        case BigInt64Array:
        case BigUint64Array:
          return this.parseBigIntTypedArray(e, r);
      }
    if (a & 1 && typeof AggregateError < "u" && (s === AggregateError || r instanceof AggregateError))
      return this.parseAggregateError(e, r);
    if (r instanceof Error)
      return this.parseError(e, r);
    if (Symbol.iterator in r || Symbol.asyncIterator in r)
      return this.parsePlainObject(e, r, !!s);
    throw new _(r);
  }
  parse(e) {
    switch (typeof e) {
      case "boolean":
        return e ? D : M;
      case "undefined":
        return Me;
      case "string":
        return T$1(e);
      case "number":
        return Ne(e);
      case "bigint":
        return Le(e);
      case "object": {
        if (e) {
          let r = this.getReference(e);
          return r.type === 0 ? this.parseObject(r.value, e) : r.value;
        }
        return Te;
      }
      case "symbol":
        return this.parseWellKnownSymbol(e);
      case "function":
        return this.parseFunction(e);
      default:
        throw new _(e);
    }
  }
};
function Pt(t, e = {}) {
  let r = Y$1(e.plugins);
  return new mt({ plugins: r, markedRefs: t.m }).deserialize(t.t);
}
var kt = class extends Rt {
  constructor(t) {
    super(t), this.mode = "cross", this.scopeId = t.scopeId;
  }
  getRefParam(t) {
    return I + "[" + t + "]";
  }
  assignIndexedValue(t, e) {
    return this.getRefParam(t) + "=" + e;
  }
  serializeTop(t) {
    let e = this.serialize(t), r = t.i;
    if (r == null)
      return e;
    let i = this.resolvePatches(), s = this.getRefParam(r), a = this.scopeId == null ? "" : I, n = i ? e + "," + i + s : e;
    if (a === "")
      return i ? "(" + n + ")" : n;
    let o = this.scopeId == null ? "()" : "(" + I + '["' + f$1(this.scopeId) + '"])';
    return "(" + this.createFunction([a], n) + ")" + o;
  }
}, Ft = class extends xt {
  constructor(t) {
    super(t), this.alive = true, this.pending = 0, this.initial = true, this.buffer = [], this.onParseCallback = t.onParse, this.onErrorCallback = t.onError, this.onDoneCallback = t.onDone;
  }
  onParseInternal(t, e) {
    try {
      this.onParseCallback(t, e);
    } catch (r) {
      this.onError(r);
    }
  }
  flush() {
    for (let t = 0, e = this.buffer.length; t < e; t++)
      this.onParseInternal(this.buffer[t], false);
  }
  onParse(t) {
    this.initial ? this.buffer.push(t) : this.onParseInternal(t, false);
  }
  onError(t) {
    if (this.onErrorCallback)
      this.onErrorCallback(t);
    else
      throw t;
  }
  onDone() {
    this.onDoneCallback && this.onDoneCallback();
  }
  pushPendingState() {
    this.pending++;
  }
  popPendingState() {
    --this.pending <= 0 && this.onDone();
  }
  parseProperties(t) {
    let e = Object.entries(t), r = [], i = [];
    for (let a = 0, n = e.length; a < n; a++)
      r.push(f$1(e[a][0])), i.push(this.parse(e[a][1]));
    let s = Symbol.iterator;
    return s in t && (r.push(this.parseWellKnownSymbol(s)), i.push(ie(this.parseIteratorFactory(), this.parse(ne$1(t))))), s = Symbol.asyncIterator, s in t && (r.push(this.parseWellKnownSymbol(s)), i.push(se$1(this.parseAsyncIteratorFactory(), this.parse(ft(t))))), s = Symbol.toStringTag, s in t && (r.push(this.parseWellKnownSymbol(s)), i.push(T$1(t[s]))), s = Symbol.isConcatSpreadable, s in t && (r.push(this.parseWellKnownSymbol(s)), i.push(t[s] ? D : M)), { k: r, v: i, s: r.length };
  }
  parsePromise(t, e) {
    return e.then((r) => {
      let i = this.parseWithError(r);
      i && this.onParse({ t: 23, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: [this.parseSpecialReference(2), i], f: void 0, b: void 0, o: void 0 }), this.popPendingState();
    }, (r) => {
      if (this.alive) {
        let i = this.parseWithError(r);
        i && this.onParse({ t: 24, i: t, s: void 0, l: void 0, c: void 0, m: void 0, p: void 0, e: void 0, a: [this.parseSpecialReference(3), i], f: void 0, b: void 0, o: void 0 });
      }
      this.popPendingState();
    }), this.pushPendingState(), this.createPromiseConstructorNode(t);
  }
  parsePlugin(t, e) {
    let r = this.plugins;
    if (r)
      for (let i = 0, s = r.length; i < s; i++) {
        let a = r[i];
        if (a.parse.stream && a.test(e))
          return re$1(t, a.tag, a.parse.stream(e, this, { id: t }));
      }
  }
  parseStream(t, e) {
    let r = ae$1(t, this.parseSpecialReference(4), []);
    return this.pushPendingState(), e.on({ next: (i) => {
      if (this.alive) {
        let s = this.parseWithError(i);
        s && this.onParse(st(t, s));
      }
    }, throw: (i) => {
      if (this.alive) {
        let s = this.parseWithError(i);
        s && this.onParse(at(t, s));
      }
      this.popPendingState();
    }, return: (i) => {
      if (this.alive) {
        let s = this.parseWithError(i);
        s && this.onParse(nt(t, s));
      }
      this.popPendingState();
    } }), r;
  }
  parseWithError(t) {
    try {
      return this.parse(t);
    } catch (e) {
      this.onError(e);
      return;
    }
  }
  start(t) {
    let e = this.parseWithError(t);
    e && (this.onParseInternal(e, true), this.initial = false, this.flush(), this.pending <= 0 && this.destroy());
  }
  destroy() {
    this.alive && (this.onDone(), this.alive = false);
  }
  isAlive() {
    return this.alive;
  }
}, Vt = class extends Ft {
  constructor() {
    super(...arguments), this.mode = "cross";
  }
};
function Ot(t, e) {
  let r = Y$1(e.plugins), i = new Vt({ plugins: r, refs: e.refs, disabledFeatures: e.disabledFeatures, onParse(s, a) {
    let n = new kt({ plugins: r, features: i.features, scopeId: e.scopeId, markedRefs: i.marked }), o;
    try {
      o = n.serializeTop(s);
    } catch (l) {
      e.onError && e.onError(l);
      return;
    }
    e.onSerialize(o, a);
  }, onError: e.onError, onDone: e.onDone });
  return i.start(t), () => {
    i.destroy();
  };
}
function P(t) {
  return { detail: t.detail, bubbles: t.bubbles, cancelable: t.cancelable, composed: t.composed };
}
var jt = { tag: "seroval-plugins/web/CustomEvent", test(t) {
  return typeof CustomEvent > "u" ? false : t instanceof CustomEvent;
}, parse: { sync(t, e) {
  return { type: e.parse(t.type), options: e.parse(P(t)) };
}, async async(t, e) {
  return { type: await e.parse(t.type), options: await e.parse(P(t)) };
}, stream(t, e) {
  return { type: e.parse(t.type), options: e.parse(P(t)) };
} }, serialize(t, e) {
  return "new CustomEvent(" + e.serialize(t.type) + "," + e.serialize(t.options) + ")";
}, deserialize(t, e) {
  return new CustomEvent(e.deserialize(t.type), e.deserialize(t.options));
} }, oe$1 = jt, Ct = { tag: "seroval-plugins/web/DOMException", test(t) {
  return typeof DOMException > "u" ? false : t instanceof DOMException;
}, parse: { sync(t, e) {
  return { name: e.parse(t.name), message: e.parse(t.message) };
}, async async(t, e) {
  return { name: await e.parse(t.name), message: await e.parse(t.message) };
}, stream(t, e) {
  return { name: e.parse(t.name), message: e.parse(t.message) };
} }, serialize(t, e) {
  return "new DOMException(" + e.serialize(t.message) + "," + e.serialize(t.name) + ")";
}, deserialize(t, e) {
  return new DOMException(e.deserialize(t.message), e.deserialize(t.name));
} }, le = Ct;
function k(t) {
  return { bubbles: t.bubbles, cancelable: t.cancelable, composed: t.composed };
}
var Dt = { tag: "seroval-plugins/web/Event", test(t) {
  return typeof Event > "u" ? false : t instanceof Event;
}, parse: { sync(t, e) {
  return { type: e.parse(t.type), options: e.parse(k(t)) };
}, async async(t, e) {
  return { type: await e.parse(t.type), options: await e.parse(k(t)) };
}, stream(t, e) {
  return { type: e.parse(t.type), options: e.parse(k(t)) };
} }, serialize(t, e) {
  return "new Event(" + e.serialize(t.type) + "," + e.serialize(t.options) + ")";
}, deserialize(t, e) {
  return new Event(e.deserialize(t.type), e.deserialize(t.options));
} }, ue = Dt, Mt = { tag: "seroval-plugins/web/File", test(t) {
  return typeof File > "u" ? false : t instanceof File;
}, parse: { async async(t, e) {
  return { name: await e.parse(t.name), options: await e.parse({ type: t.type, lastModified: t.lastModified }), buffer: await e.parse(await t.arrayBuffer()) };
} }, serialize(t, e) {
  return "new File([" + e.serialize(t.buffer) + "]," + e.serialize(t.name) + "," + e.serialize(t.options) + ")";
}, deserialize(t, e) {
  return new File([e.deserialize(t.buffer)], e.deserialize(t.name), e.deserialize(t.options));
} }, Tt = Mt;
function F(t) {
  let e = [];
  return t.forEach((r, i) => {
    e.push([i, r]);
  }), e;
}
var b$1 = {}, $t = { tag: "seroval-plugins/web/FormDataFactory", test(t) {
  return t === b$1;
}, parse: { sync() {
}, async async() {
  return await Promise.resolve(void 0);
}, stream() {
} }, serialize(t, e) {
  return e.createEffectfulFunction(["e", "f", "i", "s", "t"], "f=new FormData;for(i=0,s=e.length;i<s;i++)f.append((t=e[i])[0],t[1]);return f");
}, deserialize() {
  return b$1;
} }, Ut = { tag: "seroval-plugins/web/FormData", extends: [Tt, $t], test(t) {
  return typeof FormData > "u" ? false : t instanceof FormData;
}, parse: { sync(t, e) {
  return { factory: e.parse(b$1), entries: e.parse(F(t)) };
}, async async(t, e) {
  return { factory: await e.parse(b$1), entries: await e.parse(F(t)) };
}, stream(t, e) {
  return { factory: e.parse(b$1), entries: e.parse(F(t)) };
} }, serialize(t, e) {
  return "(" + e.serialize(t.factory) + ")(" + e.serialize(t.entries) + ")";
}, deserialize(t, e) {
  let r = new FormData(), i = e.deserialize(t.entries);
  for (let s = 0, a = i.length; s < a; s++) {
    let n = i[s];
    r.append(n[0], n[1]);
  }
  return r;
} }, ce = Ut;
function V$1(t) {
  let e = [];
  return t.forEach((r, i) => {
    e.push([i, r]);
  }), e;
}
var Bt = { tag: "seroval-plugins/web/Headers", test(t) {
  return typeof Headers > "u" ? false : t instanceof Headers;
}, parse: { sync(t, e) {
  return e.parse(V$1(t));
}, async async(t, e) {
  return await e.parse(V$1(t));
}, stream(t, e) {
  return e.parse(V$1(t));
} }, serialize(t, e) {
  return "new Headers(" + e.serialize(t) + ")";
}, deserialize(t, e) {
  return new Headers(e.deserialize(t));
} }, R = Bt, z = {}, _t = { tag: "seroval-plugins/web/ReadableStreamFactory", test(t) {
  return t === z;
}, parse: { sync() {
}, async async() {
  return await Promise.resolve(void 0);
}, stream() {
} }, serialize(t, e) {
  return e.createFunction(["d"], "new ReadableStream({start:" + e.createEffectfulFunction(["c"], "d.on({next:" + e.createEffectfulFunction(["v"], "c.enqueue(v)") + ",throw:" + e.createEffectfulFunction(["v"], "c.error(v)") + ",return:" + e.createEffectfulFunction([], "c.close()") + "})") + "})");
}, deserialize() {
  return z;
} };
function H(t) {
  let e = w$1(), r = t.getReader();
  async function i() {
    try {
      let s = await r.read();
      s.done ? e.return(s.value) : (e.next(s.value), await i());
    } catch (s) {
      e.throw(s);
    }
  }
  return i().catch(() => {
  }), e;
}
var Wt = { tag: "seroval/plugins/web/ReadableStream", extends: [_t], test(t) {
  return typeof ReadableStream > "u" ? false : t instanceof ReadableStream;
}, parse: { sync(t, e) {
  return { factory: e.parse(z), stream: e.parse(w$1()) };
}, async async(t, e) {
  return { factory: await e.parse(z), stream: await e.parse(H(t)) };
}, stream(t, e) {
  return { factory: e.parse(z), stream: e.parse(H(t)) };
} }, serialize(t, e) {
  return "(" + e.serialize(t.factory) + ")(" + e.serialize(t.stream) + ")";
}, deserialize(t, e) {
  let r = e.deserialize(t.stream);
  return new ReadableStream({ start(i) {
    r.on({ next(s) {
      i.enqueue(s);
    }, throw(s) {
      i.error(s);
    }, return() {
      i.close();
    } });
  } });
} }, x$2 = Wt;
function Z$1(t, e) {
  return { body: e, cache: t.cache, credentials: t.credentials, headers: t.headers, integrity: t.integrity, keepalive: t.keepalive, method: t.method, mode: t.mode, redirect: t.redirect, referrer: t.referrer, referrerPolicy: t.referrerPolicy };
}
var Nt = { tag: "seroval-plugins/web/Request", extends: [x$2, R], test(t) {
  return typeof Request > "u" ? false : t instanceof Request;
}, parse: { async async(t, e) {
  return { url: await e.parse(t.url), options: await e.parse(Z$1(t, t.body ? await t.clone().arrayBuffer() : null)) };
}, stream(t, e) {
  return { url: e.parse(t.url), options: e.parse(Z$1(t, t.clone().body)) };
} }, serialize(t, e) {
  return "new Request(" + e.serialize(t.url) + "," + e.serialize(t.options) + ")";
}, deserialize(t, e) {
  return new Request(e.deserialize(t.url), e.deserialize(t.options));
} }, de$1 = Nt;
function J(t) {
  return { headers: t.headers, status: t.status, statusText: t.statusText };
}
var Lt = { tag: "seroval-plugins/web/Response", extends: [x$2, R], test(t) {
  return typeof Response > "u" ? false : t instanceof Response;
}, parse: { async async(t, e) {
  return { body: await e.parse(t.body ? await t.clone().arrayBuffer() : null), options: await e.parse(J(t)) };
}, stream(t, e) {
  return { body: e.parse(t.clone().body), options: e.parse(J(t)) };
} }, serialize(t, e) {
  return "new Response(" + e.serialize(t.body) + "," + e.serialize(t.options) + ")";
}, deserialize(t, e) {
  return new Response(e.deserialize(t.body), e.deserialize(t.options));
} }, he = Lt, qt = { tag: "seroval-plugins/web/URLSearchParams", test(t) {
  return typeof URLSearchParams > "u" ? false : t instanceof URLSearchParams;
}, parse: { sync(t, e) {
  return e.parse(t.toString());
}, async async(t, e) {
  return await e.parse(t.toString());
}, stream(t, e) {
  return e.parse(t.toString());
} }, serialize(t, e) {
  return "new URLSearchParams(" + e.serialize(t) + ")";
}, deserialize(t, e) {
  return new URLSearchParams(e.deserialize(t));
} }, fe = qt, Kt = { tag: "seroval-plugins/web/URL", test(t) {
  return typeof URL > "u" ? false : t instanceof URL;
}, parse: { sync(t, e) {
  return e.parse(t.href);
}, async async(t, e) {
  return await e.parse(t.href);
}, stream(t, e) {
  return e.parse(t.href);
} }, serialize(t, e) {
  return "new URL(" + e.serialize(t) + ")";
}, deserialize(t, e) {
  return new URL(e.deserialize(t));
} }, pe = Kt;
const O = "Invariant Violation", { setPrototypeOf: Ht = function(t, e) {
  return t.__proto__ = e, t;
} } = Object;
class B extends Error {
  constructor(e = O) {
    super(typeof e == "number" ? `${O}: ${e} (see https://github.com/apollographql/invariant-packages)` : e);
    __publicField(this, "framesToPop", 1);
    __publicField(this, "name", O);
    Ht(this, B.prototype);
  }
}
function G$1(t, e) {
  if (!t)
    throw new B(e);
}
const ve = Symbol("h3Event"), A = Symbol("fetchEvent"), Zt = { get(t, e) {
  var _a;
  return e === A ? t : (_a = t[e]) != null ? _a : t[ve][e];
} };
function Jt(t) {
  return new Proxy({ request: toWebRequest(t), clientAddress: getRequestIP(t), locals: {}, [ve]: t }, Zt);
}
function Gt(t) {
  if (!t[A]) {
    const e = Jt(t);
    t[A] = e;
  }
  return t[A];
}
function Qt(t, e) {
  return new ReadableStream({ start(r) {
    Ot(e, { scopeId: t, plugins: [oe$1, le, ue, ce, R, x$2, de$1, he, fe, pe], onSerialize(i, s) {
      const a = s ? `(${Re(t)},${i})` : i;
      r.enqueue(new TextEncoder().encode(`${a};
`));
    }, onDone() {
      r.close();
    }, onError(i) {
      r.error(i);
    } });
  } });
}
async function Xt(t) {
  G$1(t.method === "POST", `Invalid method ${t.method}. Expected POST.`);
  const e = Gt(t), r = e.request, i = r.headers.get("x-server-id"), s = r.headers.get("x-server-instance"), a = new URL(r.url);
  let n, o;
  if (i)
    G$1(typeof i == "string", "Invalid server function"), [n, o] = i.split("#");
  else if (n = a.searchParams.get("id"), o = a.searchParams.get("name"), !n || !o)
    throw new Error("Invalid request");
  const l = (await globalThis.MANIFEST["server-fns"].chunks[n].import())[o];
  let u = [];
  if (!s) {
    const c = a.searchParams.get("args");
    c && JSON.parse(c).forEach((S) => u.push(S));
  }
  const d = r.headers.get("content-type");
  d.startsWith("multipart/form-data") || d.startsWith("application/x-www-form-urlencoded") ? u.push(await r.formData()) : u = Pt(await r.json(), { plugins: [oe$1, le, ue, ce, R, x$2, de$1, he, fe, pe] });
  try {
    const c = await provideRequestEvent(e, () => (sharedConfig.context = { event: e }, l(...u)));
    if (!s) {
      const S = c instanceof Error, ge = new URL(r.headers.get("referer"));
      return new Response(null, { status: 302, headers: { Location: ge.toString(), ...c ? { "Set-Cookie": `flash=${JSON.stringify({ url: a.pathname + encodeURIComponent(a.search), result: S ? c.message : c, error: S, input: [...u.slice(0, -1), [...u[u.length - 1].entries()]] })}; Secure; HttpOnly;` } : {} } });
    }
    return typeof c == "string" ? new Response(c) : (setHeader(t, "content-type", "text/javascript"), Qt(s, c));
  } catch (c) {
    return c instanceof Response && c.status === 302 ? new Response(null, { status: s ? 204 : 302, headers: { Location: c.headers.get("Location") } }) : c;
  }
}
const nr = eventHandler(Xt);

const a = [{ type: "page", $component: { src: "src/routes/[...404].tsx?pick=default&pick=$css", build: () => import('./chunks/build/_...404_.mjs'), import: () => import('./chunks/build/_...404_.mjs') }, path: "/*404", filePath: "/home/vemonet/dev/llm/libre-chat/frontend/src/routes/[...404].tsx" }, { type: "page", $component: { src: "src/routes/about.tsx?pick=default&pick=$css", build: () => import('./chunks/build/about.mjs'), import: () => import('./chunks/build/about.mjs') }, path: "/about", filePath: "/home/vemonet/dev/llm/libre-chat/frontend/src/routes/about.tsx" }, { type: "page", $component: { src: "src/routes/index.tsx?pick=default&pick=$css", build: () => import('./chunks/build/index.mjs'), import: () => import('./chunks/build/index.mjs') }, path: "/", filePath: "/home/vemonet/dev/llm/libre-chat/frontend/src/routes/index.tsx" }], g = f(a.filter((s) => s.type === "page")), h = m(a.filter((s) => s.type === "api"));
function x$1(s, n) {
  const e = s.split("/").filter(Boolean);
  e:
    for (const t of h) {
      const o = t.matchSegments;
      if (e.length < o.length || !t.wildcard && e.length > o.length)
        continue;
      for (let i = 0; i < o.length; i++) {
        const l = o[i];
        if (l && e[i] !== l)
          continue e;
      }
      const r = t[`$${n}`];
      if (r === "skip" || r === void 0)
        return;
      const c = {};
      for (const { type: i, name: l, index: p } of t.params)
        i === ":" ? c[l] = e[p] : c[l] = e.slice(p).join("/");
      return { handler: r, params: c };
    }
}
function f(s) {
  function n(e, t, o, r) {
    const c = Object.values(e).find((i) => o.startsWith(i.id + "/"));
    return c ? (n(c.children || (c.children = []), t, o.slice(c.id.length)), e) : (e.push({ ...t, id: o, path: o.replace(/\/\([^)/]+\)/g, "") }), e);
  }
  return s.sort((e, t) => e.path.length - t.path.length).reduce((e, t) => n(e, t, t.path, t.path), []);
}
function m(s) {
  return s.flatMap((n) => u(n.path).map((t) => ({ ...n, path: t }))).map(d$1).sort((n, e) => e.score - n.score);
}
function u(s) {
  let n = /(\/?\:[^\/]+)\?/.exec(s);
  if (!n)
    return [s];
  let e = s.slice(0, n.index), t = s.slice(n.index + n[0].length);
  const o = [e, e += n[1]];
  for (; n = /^(\/\:[^\/]+)\?/.exec(t); )
    o.push(e += n[1]), t = t.slice(n[0].length);
  return u(t).reduce((r, c) => [...r, ...o.map((i) => i + c)], []);
}
function d$1(s) {
  const n = s.path.split("/").filter(Boolean), e = [], t = [];
  let o = 0, r = false;
  for (const [c, i] of n.entries())
    if (i[0] === ":") {
      const l = i.slice(1);
      o += 3, e.push({ type: ":", name: l, index: c }), t.push(null);
    } else
      i[0] === "*" ? (o -= 1, e.push({ type: "*", name: i.slice(1), index: c }), r = true) : (o += 4, i.match(/^\(.+\)$/) || t.push(i));
  return { ...s, score: o, params: e, matchSegments: t, wildcard: r };
}

const T = Symbol("h3Event"), d = Symbol("fetchEvent"), U = { get(e, n) {
  var _a;
  return n === d ? e : (_a = e[n]) != null ? _a : e[T][n];
} };
function W(e) {
  return new Proxy({ request: toWebRequest(e), clientAddress: getRequestIP(e), locals: {}, [T]: e }, U);
}
function Y(e) {
  if (!e[d]) {
    const n = W(e);
    e[d] = n;
  }
  return e[d];
}
const G = " ", Q = { style: (e) => ssrElement("style", e.attrs, () => escape(e.children), true), link: (e) => ssrElement("link", e.attrs, void 0, true), script: (e) => e.attrs.src ? ssrElement("script", mergeProps(() => e.attrs, { get id() {
  return e.key;
} }), () => ssr(G), true) : null };
function b(e) {
  let { tag: n, attrs: { key: t, ...s } = { key: void 0 }, children: a } = e;
  return Q[n]({ attrs: s, key: t, children: a });
}
function V(e, n, t, s = "default") {
  return lazy(async () => {
    var _a;
    {
      const r = (await e.import())[s], f = (await ((_a = n.inputs) == null ? void 0 : _a[e.src].assets())).filter((i) => i.tag === "style" || i.attrs.rel === "stylesheet");
      return { default: (i) => [...f.map((l) => b(l)), createComponent$1(r, i)] };
    }
  });
}
function X() {
  function e(t) {
    return { ...t, ...t.$$route ? t.$$route.require().route : void 0, metadata: { ...t.$$route ? t.$$route.require().route.metadata : {}, filesystem: true }, component: V(t.$component, globalThis.MANIFEST.client, globalThis.MANIFEST.ssr), children: t.children ? t.children.map(e) : void 0 };
  }
  return g.map(e);
}
function Z(e) {
  const n = getCookie(e, "flash");
  if (!n)
    return;
  let t = JSON.parse(n);
  if (!t || !t.result)
    return [];
  const s = [...t.input.slice(0, -1), new Map(t.input[t.input.length - 1])];
  return setCookie(e, "flash", "", { maxAge: 0 }), { url: t.url, result: t.error ? new Error(t.result) : t.result, input: s };
}
async function x(e) {
  const n = globalThis.MANIFEST.client;
  return globalThis.MANIFEST.ssr, setResponseHeader(e, "Content-Type", "text/html"), Object.assign(e, { manifest: await n.json(), assets: [...await n.inputs[n.handler].assets()], initialSubmission: Z(e), routes: X(), components: { status: (s) => (setResponseStatus(e, s.code, s.text), () => setResponseStatus(e, 200)), header: (s) => (s.append ? appendResponseHeader(e, s.name, s.value) : setResponseHeader(e, s.name, s.value), () => {
    const a = getResponseHeader(e, s.name);
    if (a && typeof a == "string") {
      const r = a.split(", "), o = r.indexOf(s.value);
      o !== -1 && r.splice(o, 1), r.length ? setResponseHeader(e, s.name, r.join(", ")) : removeResponseHeader(e, s.name);
    }
  }) }, $islands: /* @__PURE__ */ new Set() });
}
function ee(e, n = {}) {
  return eventHandler({ onRequest: n.onRequest, onBeforeResponse: n.onBeforeResponse, handler: (t) => {
    const s = Y(t);
    return provideRequestEvent(s, async () => {
      const a = x$1(new URL(s.request.url).pathname, s.request.method);
      if (a) {
        const c = (await a.handler.import())[s.request.method];
        return s.params = a.params, sharedConfig.context = { event: s }, await c(s);
      }
      const r = await x(s);
      let o = { ...n };
      if (o.onCompleteAll) {
        const l = o.onCompleteAll;
        o.onCompleteAll = (c) => {
          w(r)(c), l(c);
        };
      } else
        o.onCompleteAll = w(r);
      if (o.onCompleteShell) {
        const l = o.onCompleteShell;
        o.onCompleteShell = (c) => {
          $(r, t)(), l(c);
        };
      } else
        o.onCompleteShell = $(r, t);
      const f = renderToStream(() => (sharedConfig.context.event = r, e(r)), o);
      if (r.response && r.response.headers.get("Location"))
        return sendRedirect(s, r.response.headers.get("Location"));
      const { writable: S, readable: i } = new TransformStream();
      return f.pipeTo(S), i;
    });
  } });
}
function $(e, n) {
  return () => {
    e.response && e.response.headers.get("Location") && (setResponseStatus(n, 302), setHeader(n, "Location", e.response.headers.get("Location")));
  };
}
function w(e) {
  return ({ write: n }) => {
    const t = e.response && e.response.headers.get("Location");
    t && n(`<script>window.location="${t}"<\/script>`);
  };
}
const te = ["<script", ">", "<\/script>"], ne = ["<script", ' type="module"', "><\/script>"], se = ssr("<!DOCTYPE html>");
function re(e) {
  const n = getRequestEvent();
  return createComponent(NoHydration, { get children() {
    return [se, createComponent(e.document, { get assets() {
      return n.assets.map((t) => b(t));
    }, get scripts() {
      return [ssr(te, ssrHydrationKey(), `window.manifest = ${JSON.stringify(n.manifest)}`), ssr(ne, ssrHydrationKey(), ssrAttribute("src", escape(globalThis.MANIFEST.client.inputs[globalThis.MANIFEST.client.handler].output.path, true), false))];
    } })];
  } });
}
const oe = ['<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="/favicon.ico">', "</head>"], ae = ["<html", ' lang="en">', '<body><div id="app">', "</div><!--$-->", "<!--/--></body></html>"], de = ee(() => createComponent(re, { document: ({ assets: e, children: n, scripts: t }) => ssr(ae, ssrHydrationKey(), createComponent(NoHydration, { get children() {
  return ssr(oe, escape(e));
} }), escape(n), escape(t)) }));

const handlers = [
  { route: '', handler: _f4b49z, lazy: false, middleware: true, method: undefined },
  { route: '/_server', handler: nr, lazy: false, middleware: true, method: undefined },
  { route: '/', handler: de, lazy: false, middleware: true, method: undefined }
];

function createNitroApp() {
  const config = useRuntimeConfig();
  const hooks = createHooks();
  const captureError = (error, context = {}) => {
    const promise = hooks.callHookParallel("error", error, context).catch((_err) => {
      console.error("Error while capturing another error", _err);
    });
    if (context.event && isEvent(context.event)) {
      const errors = context.event.context.nitro?.errors;
      if (errors) {
        errors.push({ error, context });
      }
      if (context.event.waitUntil) {
        context.event.waitUntil(promise);
      }
    }
  };
  const h3App = createApp({
    debug: destr(false),
    onError: (error, event) => {
      captureError(error, { event, tags: ["request"] });
      return errorHandler(error, event);
    },
    onRequest: async (event) => {
      await nitroApp.hooks.callHook("request", event).catch((error) => {
        captureError(error, { event, tags: ["request"] });
      });
    },
    onBeforeResponse: async (event, response) => {
      await nitroApp.hooks.callHook("beforeResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    },
    onAfterResponse: async (event, response) => {
      await nitroApp.hooks.callHook("afterResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    }
  });
  const router = createRouter$1({
    preemptive: true
  });
  const localCall = createCall(toNodeListener(h3App));
  const _localFetch = createFetch(localCall, globalThis.fetch);
  const localFetch = (input, init) => _localFetch(input, init).then(
    (response) => normalizeFetchResponse(response)
  );
  const $fetch = createFetch$1({
    fetch: localFetch,
    Headers: Headers$1,
    defaults: { baseURL: config.app.baseURL }
  });
  globalThis.$fetch = $fetch;
  h3App.use(createRouteRulesHandler({ localFetch }));
  h3App.use(
    eventHandler((event) => {
      event.context.nitro = event.context.nitro || { errors: [] };
      const envContext = event.node.req?.__unenv__;
      if (envContext) {
        Object.assign(event.context, envContext);
      }
      event.fetch = (req, init) => fetchWithEvent(event, req, init, { fetch: localFetch });
      event.$fetch = (req, init) => fetchWithEvent(event, req, init, {
        fetch: $fetch
      });
      event.waitUntil = (promise) => {
        if (!event.context.nitro._waitUntilPromises) {
          event.context.nitro._waitUntilPromises = [];
        }
        event.context.nitro._waitUntilPromises.push(promise);
        if (envContext?.waitUntil) {
          envContext.waitUntil(promise);
        }
      };
      event.captureError = (error, context) => {
        captureError(error, { event, ...context });
      };
    })
  );
  for (const h of handlers) {
    let handler = h.lazy ? lazyEventHandler(h.handler) : h.handler;
    if (h.middleware || !h.route) {
      const middlewareBase = (config.app.baseURL + (h.route || "/")).replace(
        /\/+/g,
        "/"
      );
      h3App.use(middlewareBase, handler);
    } else {
      const routeRules = getRouteRulesForPath(
        h.route.replace(/:\w+|\*\*/g, "_")
      );
      if (routeRules.cache) {
        handler = cachedEventHandler(handler, {
          group: "nitro/routes",
          ...routeRules.cache
        });
      }
      router.use(h.route, handler, h.method);
    }
  }
  h3App.use(config.app.baseURL, router.handler);
  const app = {
    hooks,
    h3App,
    router,
    localCall,
    localFetch,
    captureError
  };
  for (const plugin of plugins) {
    try {
      plugin(app);
    } catch (err) {
      captureError(err, { tags: ["plugin"] });
      throw err;
    }
  }
  return app;
}
const nitroApp = createNitroApp();
const useNitroApp = () => nitroApp;

const localFetch = nitroApp.localFetch;
trapUnhandledNodeErrors();

export { localFetch };
//# sourceMappingURL=index.mjs.map
