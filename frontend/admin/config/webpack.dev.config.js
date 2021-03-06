let path = require("path");
let webpack = require("webpack");
let baseConfig = require("./webpack.base.config");

module.exports = opts => {
  const { CDN_PATH, PROJECT_ROOT } = opts,
    config = baseConfig(opts),
    output_path = path.resolve(PROJECT_ROOT, "build/");

  return {
    ...config,
    mode: "development",
    devtool: "eval-source-map",
    output: {
      ...config.output,
      path: output_path,
      publicPath: "/static/wp/"
    },
    plugins: [
      ...config.plugins,
      new webpack.NoEmitOnErrorsPlugin(),
      new webpack.NamedModulesPlugin()
    ]
  };
};
