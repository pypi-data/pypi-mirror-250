# AppiumOC

AppiumOC 是围绕 appium 搭建的操作集合

***注意：当前AppiumOC是围绕 Android 实现的，因此某些方法可能无法很好的兼容iOS。***

## 调用方法
在调用之前需要自行配置 Appium Server 环境。当准备好环境之后便可以通过类似以下方法使用 AppiumOC。
```
import appium_oc

oc = appium_oc(driver)
elem = oc.find_element(oc.by.XPATH, '//*[@text=""]')
```