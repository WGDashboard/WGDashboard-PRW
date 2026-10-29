# client

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

The development server forwards `/client` requests to `http://wg.local:10086/`.
The target is configured in the tracked [proxy.js](./proxy.js) module, which must
be present even when running tests or production builds.

### Run Unit Tests

```sh
npm test
```

### Compile and Minify for Production

```sh
npm run build
```
