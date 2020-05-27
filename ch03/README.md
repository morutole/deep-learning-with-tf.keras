### cifar10_deep_with_aug.pyについて

tensorflow 2.1.0においてfit_generatorは非推奨となっている。
https://www.tensorflow.org/api_docs/python/tf/keras/Sequential#fit_generator

>Warning: THIS FUNCTION IS DEPRECATED. It will be removed in a future version. Instructions for updating: Please use Model.fit, which supports generators.  

実際ローカルの環境で実行してみると、EPOCHが進む度に下の様なエラーメッセージが出る。

> W tensorflow/core/kernels/data/generator_dataset_op.cc:103] Error occurred when finalizing GeneratorDataset iterator: Cancelled: Operation was cancelled

ググって見るとGithubで似たようなバグを報告している方はいらっしゃるが、要するに何なのかよくわからん(というか英語わからん)  
https://github.com/tensorflow/tensorflow/issues/35100

>I can verify this error with python 3.8 and python-tensorflow-opt-cuda 2.1.0rc1-2 on arch linux. This error is weirdly not present if you import only the generator from tensorflow, and everything else from Keras.  
>I realized that generator dataset is used in multi-device iterator. This seems related to newly added support for cancellation in tf.data.

tf.keras固有の問題なのかな???

https://github.com/tensorflow/tensorflow/issues/37515

>I'm using the tensorflow image tensorflow/tensorflow:2.1.0-gpu-py3 from docker hub: https://hub.docker.com/r/tensorflow/tensorflow/tags/?page=1  
>I'm also interested in consuming the fix. I'm using tf.keras.

https://github.com/tensorflow/tensorflow/pull/37877

> [TF2.2:Cherrypick]Fixing a memory leak in Keras. #37877

公式のDocumentには

>DEPRECATED:
>Model.fit now supports generators, so there is no longer any need to use this endpoint.

とあるが、これをfitで書き換える方法がわからなかった

### 4/2追記
fit_generatorは関係ない。fit_generatorをargsをそのままfitに変えるだけできちんと動いた。

手持ちのローカルだとエラーを返すが、Google Colaboratoryだとエラーは返らなかった。GPUのメモリが弱いと起こる？