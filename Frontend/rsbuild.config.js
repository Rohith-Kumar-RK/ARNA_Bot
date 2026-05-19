// @ts-check
import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';
import {pluginSvgr} from '@rsbuild/plugin-svgr';

// Docs: https://rsbuild.rs/config/
export default defineConfig({
  plugins: [pluginReact(), pluginSvgr()],
    html: {
        title: "ML Tool",
        favicon: "./public/favicon.png"
    },
    output: {
        dataUriLimit: {
            image: 1024 * 400,
            media: 0,
        },
    },
});
