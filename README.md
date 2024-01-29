# 🟧️RivetChain

This package integrates Rivet backend to Chainlit frontend, using a Rivet Node.js server, a Python client, and a Chainlit app.


## 🚀 Setup

### 1. Clone RivetChain repository

Create the root folder of the project (say, `RivetChain`), `cd` to it, then `git clone` the repository:

```
git clone https://github.com/igor2c/RivetChain.git
```

### 2. Rivet installation

`@ironclad/rivet-node` [requires](https://rivet.ironcladapp.com/docs/api-reference/node/overview) Node.js 16 or higher.

`cd` to the root folder of the project, install the `@ironclad/rivet-node` Node.js library using NPM:

```
npm install @ironclad/rivet-node
```

### 3. Express installation

`cd` to the root folder of the project, install the `express` Node.js library using NPM:

```
npm install express
```

### 4. Create `.env` file

In the root folder of the project, create a `.env` file with the following contents:

```
OPENAI_API_KEY=
LITERAL_API_KEY=
CHAINLIT_AUTH_SECRET=
```

- OPENAI_API_KEY is generated here: https://platform.openai.com/api-keys
- LITERAL_API_KEY is generated following this: https://docs.chainlit.io/data-persistence/overview
- CHAINLIT_AUTH_SECRET is generate using `chainlit create-secret`


### 5. Create Conda virtual environment

Create and activate a conda environment:

```
conda create --name rivetchain_env python=3.11
```

```
conda activate rivetchain_env
```

### 6. Chainlit installation

`chainlit` [requires](https://docs.chainlit.io/get-started/installation) `python>=3.8`.

In conda environment, install `chainlit` via pip as follows:

```
pip install chainlit
```

### 7. Run RivetChain

`cd` to the root folder of the project, and run:

```
conda activate rivetchain_env
```

```
chainlit run app.py -w
```

The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at http://localhost:8000.

## 🔧 Future updates

- **RivetChain:** `cd` to root folder of the project, `git pull origin master`
- **Rivet:** `cd` to root folder of the project (where `package.json` is located) and `npm update`
- **Chainlit:** In conda environment, `pip install chainlit --upgrade --upgrade-strategy only-if-needed` ([font](https://stackoverflow.com/a/10440459))

## ⚙️ Customization

- [Rivet Integration Getting Started](https://rivet.ironcladapp.com/docs/api-reference/getting-started-integration)
  - [Rivet GitHub](https://github.com/ironclad/rivet)
- [Chainlit Documentation](https://docs.chainlit.io/get-started/overview)
  - [Chainlit GitHub](https://github.com/Chainlit/chainlit)
   - [Chainlit Cookbook](https://github.com/Chainlit/cookbook)

