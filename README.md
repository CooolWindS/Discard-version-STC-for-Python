(Discard)Syndrome Trellis Codes for Python

[Please go new version for STC](https://github.com/CooolWindS/STC-for-python)

===

A simple way to use Syndrome Trellis Codes Steganography.
Support linux system, but does not support windows system temporarily.


Contents
---

>* [Where can use](#Environment)
>* [What is required](#Required)
>* [How to use](#Usage)
>* [What will get](#Output)
>* [Reference](#Reference)

Environment
---

>* Linux
>* Python = 3.8 or newer


Required
---

If you're using anaconda:

    $ sh ./require_conda

If you're using pip:

    $ pip install opencv
    $ pip install Pillow
    $ pip install scipy
    $ pip install pycryptodome

If you're using other ways to manage your package:

    Please ensure that the above packages are installed correctly

Usage
---

### Embed
1. Check all parameters are defined correctly in
    ```
    /lib_py/parameter.py
    ```
2. Put all images want to embed by STC in
    ```
    /files/cover/
    ```
3. Then you can start embedding
    ```
    $ python embed_main.py
    ```

### Extract
1. Check all parameters are defined correctly in
    ```
    /lib_py/parameter.py
    ```
2. Put all images want to extract message in
    ```
    /files/stego/
    ```
3. Then you can start extracting
    ```
    $ python extract_main.py
    ```

### The complete testing
1. Check all parameters are defined correctly in
    ```
    /lib_py/parameter.py
    ```
2. Put all images want to embed by STC in
    ```
    /files/cover/
    ```
3. Then you can start continuous testing
    ```
    $ sh ./shell_test
    ```

Output
---

### Embed
According to the picture format and channel selection,

```
stego picture will be placed in one or all of the following folder:
files/stego/L/
files/stego/R/
files/stego/G/
files/stego/B/
```
```
the embedded message used will be placed in the following folder:
files/message_embed/L/
files/message_embed/R/
files/message_embed/G/
files/message_embed/B/
```
```
In addition, if enabled, a log file will be generated to record the process
log_embed
```

### Extract
According to the picture format and channel selection,
```
the extracted secret message will be placed in the following folder:
files/message_extract/L/
files/message_extract/R/
files/message_extract/G/
files/message_extract/B/
```
```
In addition, if enabled, a log file will be generated to record the process
log_extract
```

### The complete testing
In addition to the output of the above two parts, there will be a comparative result information in this part. Compare whether the embedded and extracted secret messages are the same.

Use the following,
```
$ python compare_message.py
```
In addition to the output record files, statistical results will also be displayed on the screen.
```
log_compare_message
```

Reference
---
>* [Minimizing Embedding Impact in Steganography usingTrellis-Coded Quantization](http://dde.binghamton.edu/filler/pdf/Fill10spie-syndrome-trellis-codes.pdf)
>* [Syndrome-Trellis Codes Toolbox](http://dde.binghamton.edu/download/syndrome/)
>* [daniellerch/pySTC](https://github.com/daniellerch/pySTC)
