const webpack = require('webpack');

module.exports = {
  entry: './main.js',
  output: {
    path: __dirname,
    filename: 'bundle.js'
  },
  devtool: 'source-map',
  module:{
    rules:[
        {
            test:/\.css$/,
            use:['style-loader','css-loader']
        }
   ]
  },
  watch: true
};
