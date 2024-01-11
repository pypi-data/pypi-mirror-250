# Radiant-Compiler

Pull the image with the environ for [python-for-android](https://python-for-android.readthedocs.io/en/latest/) that includes the [Android NDK](https://developer.android.com/studio/projects/install-ndk) and the [SDK](https://developer.android.com/studio) to compile Python applications into APKs installer:


```python
docker pull yeisondev/radiant:compiler
```

Then install the Python pacakge to use the ```p4a``` command:


```python
pip install radiant-compiler
```

Now ```p4a``` is replaced by ```docker_p4a```


```python
docker_p4a apk --arch arm64-v8a
```

## Software versions included in the image


```python
ARG NDK_VERSION=r23b
SDK_VERSION=8512546_latest 
JAVA_VERSION=jdk17-openjdk
NDKAPI=27
ANDROIDAPI=27
```
