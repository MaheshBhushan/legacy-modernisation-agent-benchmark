export type Response = {ok:false;error:{code:string;field:string}} | {ok:true;profile:string;effectiveSampleMs:number;readingMilli:number;status:string;warnings:string[]};
export function evaluate(input: unknown): Response {
  const fields = ['profile','sampleMs','gain','offsetMilli','rawMilli','alarmLowMilli','alarmHighMilli','enabled'];
  const fail = (field:string):Response => ({ok:false,error:{code:'INVALID_REQUEST',field}});
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).length !== fields.length || fields.some(f=>!Object.hasOwn(input,f))) return fail('$');
  const v = input as Record<string,unknown>;
  const ranges:Record<string,[number,number]>={sampleMs:[10,60000],gain:[1,16],offsetMilli:[-100000,100000],rawMilli:[-1000000,1000000],alarmLowMilli:[-20000000,20000000],alarmHighMilli:[-20000000,20000000]};
  for(const f of fields){
    if(f==='profile'){if(v[f]!=='temperature'&&v[f]!=='pressure')return fail(f);}
    else if(f==='enabled'){if(typeof v[f]!=='boolean')return fail(f);}
    else {const n=v[f]; const [lo,hi]=ranges[f]!; if(typeof n!=='number'||!Number.isSafeInteger(n)||n<lo||n>hi)return fail(f);}
  }
  const n=v as Record<string,number>;
  if(n['alarmLowMilli']!>=n['alarmHighMilli']!)return fail('alarmHighMilli');
  const effectiveSampleMs=Math.ceil(n['sampleMs']!/10)*10;
  const raw=n['rawMilli']!*n['gain']!+n['offsetMilli']!;
  const readingMilli=Math.max(v['profile']==='temperature'?-40000:0,Math.min(v['profile']==='temperature'?125000:1000000,raw));
  const warnings:string[]=[];
  if(effectiveSampleMs!==v['sampleMs'])warnings.push('sample-rounded');
  if(readingMilli!==raw)warnings.push('reading-clamped');
  return {ok:true,profile:v['profile'] as string,effectiveSampleMs,readingMilli,status:!v['enabled']?'disabled':readingMilli<n['alarmLowMilli']!?'low':readingMilli>n['alarmHighMilli']!?'high':'ok',warnings};
}
