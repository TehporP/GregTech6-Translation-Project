# GregTech6-Translation-Project
格雷科技6 汉化工程

这次使用字典替换的方法来汉化格雷

字典替换器使用方法

    python3 DictMapper.py [Dictionary File] [Source File] [Translated File] [UnTranslated Strings]
    四个参数缺一不可，如一个参数也不加就等同于
    python3 DictMapper.py Dicts.tml GregTech\_en.txt GregTech\_cn.txt UnTranslated.txt

字典替换器硬编码的功能:

- 自动替换复数单词
- 强制替换单词开头的`Anti-`，如字典中无条目则报错
- 自动替换形如`Carbon-14`的同位素表示
- 只替换以`S:` 开头的行

字典文件样例

    Beer: 啤      #全局字典条目
    Coffee: 咖啡
    Dark: 黑
    Block of: 块
    Sodium: 钠
    Dust: 粉末

    '$^fluid\.potion\.darkcoffee$': #以“$”开头的是分组条目，不能嵌套
        Dark: 清  #分组字典条目
    '$gt\.meta\.storage\.dust.*':
        '#(Block of)(.+)': '{0[1]}{0[0]}' #以“#”开头的是正则匹配条目，用于语序的特殊处理，也可放在分组条目中

输入样例

    languagefile {
        S:fluid.potion.darkbeer=Dark Beers
        S:fluid.potion.darkcoffee=Dark Coffee
        S:gt.meta.storage.dust.110.name=Block of Sodium Dust
        S:very.strange.line=Block of Sodium Dust
    }

输出结果

    languagefile {
        S:fluid.potion.darkbeer=黑啤
        S:fluid.potion.darkcoffee=清咖啡
        S:gt.meta.storage.dust.110.name=钠粉末块
        S:very.strange.line=块钠粉末
    }

旧的JavaScript字典替换器作者:wdhwg001  
地址:[http://libertydomemod.b0.upaiyun.com/index.html](http://libertydomemod.b0.upaiyun.com/index.html)  
YAML检查器地址:[http://nodeca.github.io/js-yaml/](http://nodeca.github.io/js-yaml/)
