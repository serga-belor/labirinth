module.exports = {
    "env": {
        "browser": true,
        "es2021": true,
        "node": true
    },
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": 2015,
        "ecmaFeatures": {
            "jsx": true
        },
        "sourceType": "module",
        "project": "./site/tsconfig.json"
    },
    "plugins": ["@typescript-eslint"],
    "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended"
    ],
    "rules": {
        "quotes": [ "error", "double"],
        "@typescript-eslint/quotes": ["error", "double"],
        "semi": ["error", "always"],
        "no-trailing-spaces": "error",
        "eol-last": ["error", "always"],
        "no-multiple-empty-lines": ["error", { "max": 2 }],
        "comma-dangle": ["error", "never"]
    }
};
