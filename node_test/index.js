const fetch=require('isomorphic-fetch');

let done='201,202,205,254,301,302,302B,303,303se,304N,305,308,309,309S,310,310S,314,316,316L,316F,316N,317,317L,321,329,330,334,347,348,384,405,409,429,430,430F,430FSe,434,436,442,446,403,410,414,416,416Se,420,420F,422,431,440A,440B,440C,501,502,630,304,304L,'
// 201~303se 53/7
// 304N~310 69/13
// 310S~316N 44/45
// 317~384 62/33
// 405~429 16/4
// 430 430F total 31
// 430FSe x
// 434~410 66/6 
// 414~416Se 36/1
// 420~440B 43/38
// 440C~304L 57/52
// 304Cu 1/0

let list = '304Cu'
list=list.split(',');
const batch=3;
const batch_list=list.reduce((cur,e,i)=>{
    let idx=(i-i%batch)/batch;
    if(i%batch===0){
        cur.push([e])
    }else{
        cur[idx].push(e)
    }
    // console.log(cur,e,i);
    return cur;
},[])
const len=list.length;
const batch_len=batch_list.length;

// console.log(list_new)
const sleep=(ms)=>{
    return new Promise(resolve => setTimeout(resolve, ms));
}
let total={ok:0,err:0};
const root='http://localhost:8000/crawl/';

const run = async ()=>{
    for await(let e of batch_list){  
        console.log(e);
        await Promise.all([fetchingPromise(root+e[0]),fetchingPromise(root+e[1]),fetchingPromise(root+e[2])])
        console.log(total)
        await sleep(10000);
        if(total.ok+total.err>99){
            console.log(new Date())
            break
            // await sleep(1000*60*6)
        }
    }
    console.log(total)
}
const fetchingPromise=async (url)=>{
    const result=await fetch(url);
    const json_str=await result.text();
    const json=await JSON.parse(json_str);
    // const json={
    //     ok:10,
    //     err:1,
    //     blocked:false,
    // }
    if(json.blocked===true){
        console.log('blocked');
        return false;
    }else{
        total.ok+=json.ok;
        total.err+=json.err;
        return true;
    }
}

run()