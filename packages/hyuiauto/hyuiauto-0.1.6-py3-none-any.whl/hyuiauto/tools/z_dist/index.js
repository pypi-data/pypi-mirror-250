let root

const hash_router = {
  '/androidtool'      : '/androidtool.js',
  '/charger'   : {fileName: '/device.js', className:'Charger'},
}

let hashEntries = Object.entries(hash_router)

const ModuleFile2Element = {} 

async function routerChanged(){
  let url = window.location.hash.slice(1)

  let componentDesc = null // 组件描述

  console.log('route url is', url)

  //  使用for ... of 遍历数组
  for (let [key, value] of hashEntries) {
    if (url.startsWith(key)){
      componentDesc = value
      break
    }    
  }

  // hash_router中没有该配置
  if (!componentDesc){
    alert('该功能未实现')
    return
  }

  
  // 尝试从表中获取已经 创建 的 jsx element
  let element = ModuleFile2Element[url]

  // 未加载过
  if (!element) {    
    // 只是模块文件路径， 组件肯定是缺省导出
    if(typeof componentDesc === 'string'){
      // let { default: DClass }  = await import(componentDesc);
      // Component = DClass
      Component  = (await import(componentDesc)).default;
    }
    // 否则，是命名导出
    else{
      Component  = (await import(componentDesc.fileName))[componentDesc.className]
    }

    element = React.createElement(Component)
    
    ModuleFile2Element[url] = element
  }  

  root.render(element);

}

window.onload = function(){
  
  // todo 只要hash 变化就从root开始render， 效率有问题，
  //      应该找到变化开始的那一层的element，调用render
  //  比如 /a/b/c 变为 /a/e/f, 应该调用 a 对应的 element 的render， 而不是root的render
  //  比如 /a/b/c 变为 /a/b/f, 应该调用 b 对应的 element 的render， 而不是root的render
  window.addEventListener('hashchange', function() {
    routerChanged()
  });
  
  root = ReactDOM.createRoot(document.querySelector('main'));
  
  routerChanged();


}

