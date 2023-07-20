# bangumi-auto-sorting
将RSS下载的番剧自动分类为jellyfin可识别的目录树  

![image](https://github.com/hhhfsj/bangumi-auto-sorting/assets/47785500/89566169-053d-45d5-81f5-5da0c2f44b02)

``` dir tree
动画
├── 狼与香辛料
│   ├── S00
│   │   └── S00E01 - 狼与香辛料的原视频文件名.mkv
│   ├── S01
│   │   ├── S01E01 - 狼与香辛料的原视频文件名.mkv
│   │   └── ……
│   └── S02
│       ├── S02E01 - 狼与香辛料的原视频文件名.mkv
│       └── ……
└── ……
```

请按需修改config.json内容后运行
``` json

// 该文件仅为参考，在实际填写时请删除注释

{
	"sleep_time": 30, //等待时间（秒）
	"debug": true, //调试模式
	"Configs": [ //配置列表
		{
			"Model": "File_name", // 获取方式（可选：File_name|Anitomy）
			"input_dir": "input", // 输入文件夹
			"output_dir": "output", // 输出文件夹
			"Season_add_zero": false, // 是否给1加0
			"Copy_model": true, // 是否启用复制模式
			"Del_original_file": false // 是否删除源文件（仅复制模式）
		},
		{
			"Model": "Anitomy",
			"input_dir": "input",
			"output_dir": "output",
			"Season_add_zero": false,
			"Copy_model": true,
			"Del_original_file": false
		}
	]
}
```
