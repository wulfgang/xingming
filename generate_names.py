import itertools

# 给定的两个数组，array1包含单字汉字，array2包含其他汉字
array1 = ["星","初","锦","宸","然","悦","思","书","楚","晨","诗","舒","承","瑞","睿","千","歌","心","柔","姝","瑜","美","如","靖","时","静","秋","纯","昔","紫","斯","西","馨","新","钧","俞","善","笑","惜","尚","理","穆","慈","钰","暄","稀","裕","童","聪","珊","疏","诚","叙","声","正","锐","婵","施","宣","儒","春","净","喻"]
array2 = ["泽","沐","希","子","洛","禾","清","云","慕","熙","墨","澄","妍","雨","凡","沁","溪","涵","文","博","恒","妤","霖","沫","白","牧","航","浩","米","明","淮","浠","煦","贝","潇","和","凝","怀","澈","润","淳","渝","沛","翰","鸣","漾","泓","雪","曼","风","湉","闻","渊","向","含","洪","沂","漫","弘","鸿","霏","滢","露"]

with open('mz_values.txt', 'w') as f:
    # 使用itertools.product生成所有可能的组合
    for first, second in itertools.product(array1[10:], array2[10:]):
        # 组合两个汉字，形成名字
        name = f"{first}{second}"
        #print(name)
        f.write(name + '，')
    #f.write('\n')
    for first, second in itertools.product(array2[10:], array1[10:]):
        # 组合两个汉字，形成名字
        name = f"{first}{second}"
        #print(name)
        f.write(name + '，')