from modules.configs.MyConfig import MyConfigger

# 构造一个config，用于在tab间共享softwareconfigdict
gui_shared_config = MyConfigger()
gui_shared_config.save_software_config() # 保存下全局的softwareconfigdict，以记录版本变更
# 用于注入到配置页面的js，使tab内容间滚动
injectJSforTabs = """
<script>
// 节流 立刻执行后等待delay再接受
function throttle(func, delay) {
    let timer = null; // 定时器
    return function (...args) {
        if (!timer) {
            func.apply(this, args); // 执行方法
            timer = setTimeout(() => {
                timer = null; // 清空定时器，允许下一次调用
            }, delay);
        }
    };
}

// 阻止input上的滚动
function preventInputScroll(event){
    if (event.target.tagName.toLowerCase() === "input") { event.preventDefault() }
}

// 监听 scrollBoxElement 的滚轮滚动事件
function handleScroll(event) {
    // 获取子元素（假设内部子元素是第一个子元素）也就是有scroll这个class的div
    const childElement = document.querySelector(".locscroll").querySelector("*");
    console.log(event);

    // 获取子元素的滚动位置属性
    const { scrollTop, scrollHeight, clientHeight } = childElement;

    // 找到tags元素们
    const tagsElements = document.querySelector(".loctabs").children[0].querySelectorAll(".q-tab");

    const findNowSelectedTab = () => {
        for(let i of tagsElements.keys()){
            if(tagsElements[i].getAttribute("aria-selected")=="true"){
                return i;
            }
        }
        return -1;
    }

    if (event.deltaY > 0) {
        // 向下滚动，由于tab底部有200px空白，边距小于20的时候就可以判定为用户想往下一个tab滚了
        if (scrollTop + clientHeight >= scrollHeight - 20) {
            console.log("Touch Head.");
            const nowIndTab = findNowSelectedTab();
            console.log(nowIndTab);
            if (nowIndTab !== -1 && nowIndTab!==tagsElements.length-1){
                tagsElements[nowIndTab+1].click();
                event.preventDefault();
            }
        }
    } else if (event.deltaY < 0) {
        // 向上滚动
        if (scrollTop <= 0) {
            console.log("Touch Foot.");
            const nowIndTab = findNowSelectedTab();
            console.log(nowIndTab);
            if (nowIndTab !== -1 && nowIndTab!==0){
                tagsElements[nowIndTab-1].click();
                event.preventDefault();
            }
        }
    }
}
window.addEventListener("load", ()=>{
    if(!window.jsinjected){
        const scrollBoxElement = document.querySelector(".locscroll");
        const throttledHandleScroll = throttle(handleScroll, 400);
        
        scrollBoxElement.addEventListener("wheel", throttledHandleScroll);
        scrollBoxElement.addEventListener("wheel", preventInputScroll);
        window.jsinjected = true;
        console.log("JS is injected");
    }
})

</script>
"""