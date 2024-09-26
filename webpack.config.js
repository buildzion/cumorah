'use strict'

const path = require('path')
const autoprefixer = require('autoprefixer')
const miniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    mode: 'development',
    entry: './src/js/main.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'cumorah/static/bundle')
    },
    plugins: [
        new miniCssExtractPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    {
                        // loader: 'style-loader'
                        loader: miniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [autoprefixer]
                            }
                        }
                    },
                    {
                        loader: 'sass-loader'
                    }
                ]
            }
        ]
    }
}
