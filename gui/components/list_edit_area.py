from nicegui import ui
from modules.configs.MyConfig import config

def list_edit_area(datadict, linedesc, blockdesc=""):
    """
    datadict: 要修改的二维或三维列表，长度代表列表维度
        [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
    linedesc: 二维或三维列表的描述，长度代表列表维度
    blockdesc: 对于这个块的描述
    """
    dim = len(linedesc)
    subdim = 0
    if dim >= 3:
        subdim = len(linedesc[2])
    @ui.refreshable
    def item_list():
        for blocklinedesc in blockdesc.split('\n'):
            ui.label(f'{blocklinedesc}')
        for i in range(len(datadict)):
            line_item = datadict[i]
            ui.label(f'{config.get_text("config_nth")} {i+1} {linedesc[0]}: ')
            with ui.row():
                for j in range(len(line_item)):
                    if len(linedesc) == 2:
                        # 第几个教室
                        ui.number(f'{linedesc[1]}',
                                    min=1,
                                    step=1,
                                    precision=0,
                                    format="%.0f",
                                    value=line_item[j],
                                    on_change=lambda v,i=i,j=j: datadict[i].__setitem__(j, int(v.value)),
                                    ).style('width: 60px')
                    elif len(linedesc) == 3:
                        ui.label(f'{linedesc[1]}:')
                        with ui.row():
                            with ui.card():
                                for k in range(len(line_item[j])):
                                    #  遍历关卡和次数
                                    min_value = 1
                                    if k == subdim-1:
                                        min_value = -99
                                    ui.number(f'{linedesc[2][k]}',
                                                min=min_value,
                                                step=1,
                                                precision=0,
                                                format="%.0f",
                                                value=line_item[j][k],
                                                on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                ).style('width: 60px')
                    elif len(linedesc) == 4:
                        ui.label(f'{linedesc[1]}:')
                        with ui.row():
                            with ui.card():
                                # 遍历每一列中的每一关和次数
                                for k in range(len(line_item[j])):
                                    #  遍历关卡和次数
                                    # 获取最小值
                                    min_value = 1
                                    if k == len(linedesc)-2:
                                        min_value = -99
                                    if k == len(linedesc)-1 and k >= 3:
                                        ui.switch(value=line_item[j][k],on_change=lambda v,i=i,j=j:datadict[i][j].__setitem__(k, bool(v.value)))
                                        continue
                                    ui.number(f'{linedesc[2][k]}',
                                                min=min_value,
                                                step=1,
                                                precision=0,
                                                format="%.0f",
                                                value=line_item[j][k],
                                                on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                ).style('width: 60px')
                with ui.column():
                    ui.button(f"{config.get_text('button_add')} {linedesc[1]}", on_click=lambda i=i: add_item_item(i))
                    if len(datadict[i]) > 0:
                        ui.button(f"{config.get_text('button_delete')} {linedesc[1]}", on_click=lambda i=i: del_item_item(i), color="red")
        with ui.row():
            ui.button(f"{config.get_text('button_add')} {linedesc[0]}", on_click=add_item)
            if len(datadict) > 0:
                ui.button(f"{config.get_text('button_delete')} {linedesc[0]}", on_click=del_item, color="red")
 
    def add_item():
        datadict.append([])
        item_list.refresh()
    
    def del_item():
        datadict.pop()
        item_list.refresh()
    
    def add_item_item(item_ind):
        if dim == 2:
            datadict[item_ind].append(1)
        elif dim == 3:
            if subdim == 2:
                datadict[item_ind].append([1, 1])
            elif subdim == 3:
                datadict[item_ind].append([1, 1, 1])
        # 给活动/普通关卡/困难/学园交流会/特殊任务/悬赏通缉，增加快捷开关
        if dim >= 3 and subdim == 4:
            datadict[item_ind].append([1, 1, 1,True])
        
        item_list.refresh()
    
    def del_item_item(item_ind):
        datadict[item_ind].pop()
        item_list.refresh()

    item_list()