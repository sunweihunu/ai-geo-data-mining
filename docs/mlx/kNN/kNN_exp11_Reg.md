# kNN_exp11_Reg.mlx

「k 最近邻（kNN）」目录 · 对应书稿 **第07章 k最近邻（kNN）模型** · 18.3 KB · 代码 30 行 · 图窗 1

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/kNN/kNN_exp11_Reg.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../../src/kNN/kNN_exp11_Reg.mlx" download>下载 kNN_exp11_Reg.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页展示脚本内的文字说明与代码，并嵌入由 MATLAB `export` 命令从 .mlx 导出的运行结果——命令行输出与图窗均取自作者在实时脚本中保存的内容。「复制代码」仅复制脚本代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

**根据病人的年龄和身高预测血压最高值**

采用kNN解决回归问题 具体使用knnsearch和mean

## 脚本内容

```matlab
% 根据病人的年龄和身高预测血压最高值
% 采用kNN解决回归问题
% 具体使用knnsearch和mean
```

## 导入医院数据集

```matlab
load hospital;

disp(hospital)  % 展示一下hospital的内容
```

<pre class="mlx-out">               LastName              Sex       Age    Weight    Smoker    BloodPressure      Trials             
    YPL-320    {'SMITH'     }        Male      38     176       true      124          93    {[         18]}    
    GLI-532    {'JOHNSON'   }        Male      43     163       false     109          77    {[   11 13 22]}    
    PNI-258    {'WILLIAMS'  }        Female    38     131       false     125          83    {1x0 double   }    
    MIJ-579    {'JONES'     }        Female    40     133       false     117          75    {[       6 12]}    
    XLK-030    {'BROWN'     }        Female    49     119       false     122          80    {[      14 23]}    
    TFP-518    {'DAVIS'     }        Female    46     142       false     121          70    {[         19]}    
    LPD-746    {'MILLER'    }        Female    33     142       true      130          88    {[         13]}    
    ATA-945    {'WILSON'    }        Male      40     180       false     115          82    {1x0 double   }    
    VNL-702    {'MOORE'     }        Male      28     183       false     115          78    {[          2]}    
    LQW-768    {'TAYLOR'    }        Female    31     132       false     118          86    {[         11]}    
    QFY-472    {'ANDERSON'  }        Female    45     128       false     114          77    {[    8 10 14]}    
    UJG-627    {'THOMAS'    }        Female    42     137       false     115          68    {[        4 9]}    
    XUE-826    {'JACKSON'   }        Male      25     174       false     127          74    {1x0 double   }    
    TRW-072    {'WHITE'     }        Male      39     202       true      130          95    {[          8]}    
    ELG-976    {'HARRIS'    }        Female    36     129       false     114          79    {1x0 double   }    
    KOQ-996    {'MARTIN'    }        Male      48     181       true      130          92    {[13 15 21 27]}    
    YUZ-646    {'THOMPSON'  }        Male      32     191       true      124          95    {1x0 double   }    
    XBR-291    {'GARCIA'    }        Female    27     131       true      123          79    {1x0 double   }    
    KPW-846    {'MARTINEZ'  }        Male      37     179       false     119          77    {1x0 double   }    
    XBA-581    {'ROBINSON'  }        Male      50     172       false     125          76    {[   20 26 30]}    
    BKD-785    {'CLARK'     }        Female    48     133       false     121          75    {[   20 23 28]}    
    JHV-416    {'RODRIGUEZ' }        Female    39     117       false     123          79    {1x0 double   }    
    VWL-936    {'LEWIS'     }        Female    41     137       false     114          88    {[          8]}    
    AAX-056    {'LEE'       }        Female    44     146       true      128          90    {1x0 double   }    
    DTT-578    {'WALKER'    }        Female    28     123       true      129          96    {[          7]}    
    FZR-250    {'HALL'      }        Male      25     189       false     114          77    {[        1 5]}    
    FZI-843    {'ALLEN'     }        Female    39     143       false     113          80    {[        3 9]}    
    PUE-347    {'YOUNG'     }        Female    25     114       false     125          76    {[          5]}    
    HLE-603    {'HERNANDEZ' }        Male      36     166       false     120          83    {[        3 7]}    
    FME-049    {'KING'      }        Male      30     186       true      127          89    {[          3]}    
    AFK-336    {'WRIGHT'    }        Female    45     126       true      134          92    {[13 20 23 25]}    
    TQW-430    {'LOPEZ'     }        Female    40     137       false     121          83    {1x0 double   }    
    LIM-480    {'HILL'      }        Female    25     138       false     115          80    {[          2]}    
    YYV-570    {'SCOTT'     }        Male      47     187       false     127          84    {[          8]}    
    MSL-692    {'GREEN'     }        Male      44     193       false     121          92    {1x0 double   }    
    KKL-155    {'ADAMS'     }        Female    48     137       false     127          83    {1x0 double   }    
    WTL-804    {'BAKER'     }        Male      44     192       true      136          90    {[         21]}    
    NGK-757    {'GONZALEZ'  }        Female    35     118       false     117          85    {[        1 4]}    
    FLX-785    {'NELSON'    }        Male      33     180       true      124          90    {[    6 10 13]}    
    RYA-895    {'CARTER'    }        Female    38     128       false     120          74    {[         18]}    
    VRH-620    {'MITCHELL'  }        Male      39     164       true      128          92    {1x0 double   }    
    AFB-271    {'PEREZ'     }        Male      44     183       false     116          80    {[      12 19]}    
    RVS-253    {'ROBERTS'   }        Male      44     169       true      132          89    {1x0 double   }    
    JQQ-692    {'TURNER'    }        Male      37     194       true      137          96    {[       3 13]}    
    VDZ-577    {'PHILLIPS'  }        Male      45     172       false     117          89    {[10 15 17 19]}    
    NFO-023    {'CAMPBELL'  }        Female    37     135       false     116          77    {1x0 double   }    
    SPK-046    {'PARKER'    }        Male      30     182       false     119          81    {[        1 3]}    
    LQF-219    {'EVANS'     }        Female    39     121       false     123          76    {[         12]}    
    HJQ-495    {'EDWARDS'   }        Male      42     158       false     116          83    {[         15]}    
    EOT-439    {'COLLINS'   }        Male      42     179       true      124          78    {[     4 6 10]}    
    FLJ-908    {'STEWART'   }        Male      49     170       true      129          95    {[         15]}    
    RBA-579    {'SANCHEZ'   }        Female    44     136       true      130          91    {[         12]}    
    HAK-381    {'MORRIS'    }        Female    43     135       true      132          91    {[    3 12 20]}    
    OIT-428    {'ROGERS'    }        Female    47     147       false     117          86    {[      25 26]}    
    DAU-529    {'REED'      }        Male      50     186       true      129          89    {[         22]}    
    SJX-191    {'COOK'      }        Female    38     124       false     118          79    {[          9]}    
    JRV-811    {'MORGAN'    }        Female    41     134       false     120          74    {[      14 18]}    
    WCJ-997    {'BELL'      }        Male      45     170       true      138          82    {[          7]}    
    WAQ-577    {'MURPHY'    }        Male      36     180       false     117          76    {[        2 6]}    
    PPT-086    {'BAILEY'    }        Female    38     130       false     113          81    {[      1 8 9]}    
    MPF-827    {'RIVERA'    }        Female    29     130       false     122          77    {1x0 double   }    
    XAX-646    {'COOPER'    }        Female    28     127       false     115          73    {[        4 5]}    
    VAO-708    {'RICHARDSON'}        Female    30     141       false     120          85    {1x0 double   }    
    QEQ-082    {'COX'       }        Female    28     111       false     117          76    {1x0 double   }    
    VPG-454    {'HOWARD'    }        Female    29     134       false     123          80    {[          4]}    
    RBO-332    {'WARD'      }        Male      36     189       false     123          80    {[          1]}    
    IJY-130    {'TORRES'    }        Female    45     137       false     119          79    {1x0 double   }    
    HQI-880    {'PETERSON'  }        Female    32     136       false     110          82    {[          8]}    
    ISR-838    {'GRAY'      }        Female    31     130       false     121          79    {1x0 double   }    
    NSK-403    {'RAMIREZ'   }        Female    48     137       true      138          82    {[          9]}    
    SCQ-914    {'JAMES'     }        Male      25     186       false     125          75    {[      1 3 5]}    
    ILS-109    {'WATSON'    }        Female    40     127       true      122          91    {[          6]}    
    VLK-852    {'BROOKS'    }        Male      39     176       false     120          74    {1x0 double   }    
    OJK-718    {'KELLY'     }        Female    41     127       false     117          78    {[      16 19]}    
    JDR-456    {'SANDERS'   }        Female    33     115       true      125          85    {[     4 7 11]}    
    SRV-618    {'PRICE'     }        Male      31     178       true      124          84    {[       1 11]}    
    OSJ-974    {'BENNETT'   }        Female    35     131       false     121          75    {[         12]}    
    LSL-639    {'WOOD'      }        Male      32     183       false     118          78    {[          7]}    
    SMP-283    {'BARNES'    }        Male      42     194       false     120          81    {[         11]}    
    QOO-305    {'ROSS'      }        Female    48     126       false     118          79    {1x0 double   }    
    UDS-151    {'HENDERSON' }        Male      34     186       false     118          85    {[        1 2]}    
    YLN-495    {'COLEMAN'   }        Male      39     188       false     122          79    {[   4 7 8 12]}    
    NSU-424    {'JENKINS'   }        Male      28     189       true      134          82    {[          3]}    
    WXM-486    {'PERRY'     }        Female    29     120       false     131          80    {[        1 7]}    
    EHE-616    {'POWELL'    }        Female    32     132       false     113          80    {[          5]}    
    ZGS-009    {'LONG'      }        Male      39     182       true      125          92    {[          9]}    
    HWZ-321    {'PATTERSON' }        Female    37     120       true      135          92    {[        1 5]}    
    GGU-691    {'HUGHES'    }        Female    49     123       true      128          96    {[   14 24 25]}    
    WUS-105    {'FLORES'    }        Female    31     141       true      123          87    {[          7]}    
    TXM-629    {'WASHINGTON'}        Female    37     129       false     122          81    {[     3 8 12]}    
    DGC-290    {'BUTLER'    }        Male      38     184       true      138          90    {[      16 18]}    
    AGR-528    {'SIMMONS'   }        Male      45     181       false     124          77    {[    8 18 25]}    
    XBJ-540    {'FOSTER'    }        Female    30     124       false     130          91    {[          1]}    
    FCD-425    {'GONZALES'  }        Male      48     174       false     123          79    {1x0 double   }    
    HQO-561    {'BRYANT'    }        Female    48     134       false     129          73    {[         24]}    
    REV-997    {'ALEXANDER' }        Male      25     171       true      128          99    {[          1]}    
    HVR-372    {'RUSSELL'   }        Male      44     188       true      124          92    {[         22]}    
    MEZ-469    {'GRIFFIN'   }        Male      49     186       false     119          74    {[          9]}    
    BEZ-311    {'DIAZ'      }        Male      45     172       true      136          93    {1x0 double   }    
    ZZB-405    {'HAYES'     }        Male      48     177       false     114          86    {[         28]}</pre>

```matlab
X = [hospital.Age hospital.Weight];
Y= hospital.BloodPressure(:,1);
```

## Case 1 对5个病人进行预测，没有高血压的真值

```matlab
X_new = [20 162; 30 169; 40 168; 50 170; 60 171];   % 5个新病人

% 默认的knnsearch
Idx = knnsearch(X,X_new);
% Find the patients in X closest in age and weight to those in Y.
X(Idx,:)
```

<pre class="mlx-out">ans = 5x2
    25   171
    25   171
    39   164
    49   170
    50   172</pre>

```matlab
Y_pre1=mean(Y(Idx),2)  %最近邻的Y的平均值
```

<pre class="mlx-out">Y_pre1 = 5x1
   128
   128
   128
   129
   125</pre>

```matlab
% 改变knnsearch参数
Idx2 = knnsearch(X,X_new,'K',2,'Distance','minkowski','P',5);
X(Idx2(:,1),:)  % 第1个最近邻的X
```

<pre class="mlx-out">ans = 5x2
    25   171
    25   171
    39   164
    49   170
    50   172</pre>

```matlab
X(Idx2(:,2),:)  % 第2个最近邻的X
```

<pre class="mlx-out">ans = 5x2
    25   174
    25   174
    44   169
    50   172
    49   170</pre>

```matlab
Y_pre2=mean(Y(Idx2),2)  %最近邻的Y的平均值
```

<pre class="mlx-out">Y_pre2 = 5x1
  127.5000
  127.5000
  130.0000
  127.0000
  127.0000</pre>

```matlab
% 比较一下结果
[Y_pre1 Y_pre2]
```

<pre class="mlx-out">ans = 5x2
  128.0000  127.5000
  128.0000  127.5000
  128.0000  130.0000
  129.0000  127.0000
  125.0000  127.0000</pre>

## Case 2 对所有数据集进行预测

采用knnsearch和自取平均值方法

```matlab
kk=2
```

<pre class="mlx-out">kk = 2</pre>

```matlab
Idx3 = knnsearch(X,X,'K',kk);
Y_pre3=mean(Y(Idx3),2)
```

<pre class="mlx-out">Y_pre3 = 100x1
  122.0000
  118.5000
  119.0000
  118.5000
  125.0000
  124.5000
  126.5000
  119.5000
  117.0000
  115.5000</pre>

```matlab
% 比较结果
figure;
plot(Y,Y_pre3,'*');
```

<img src="../kNN_exp11_Reg_media/figure_0.png" alt="图窗 1" loading="lazy" />
