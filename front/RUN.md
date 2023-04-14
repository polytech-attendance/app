# Установка

1. Установить [`npm`](https://www.npmjs.com/). Для Windows стоит использовать [nvm-windows](https://github.com/coreybutler/nvm-windows#installation--upgrades) (по ссылке гайд по установке)
<!--
npm create svelte@latest .
-->
2. Выполнить `npm install` в этой папке (`front`) --- эта команда установит зависимости.

# Запуск

## Разработка

Чтобы запустить development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

При успешном запуске откроется страница <http://localhost:5173/> в браузере.

## Сборка

Чтобы создать production версию, нужно выполнить

```bash
npm run build
```

Можно запустить превью production сборки с помощью команды `npm run preview`.
