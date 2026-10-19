import { spawn } from 'node:child_process';
const children = [spawn(process.execPath,['node_modules/astro/bin/astro.mjs','dev','--host','127.0.0.1'],{stdio:'inherit'}),spawn(process.execPath,['scripts/cms.mjs'],{stdio:'inherit'})];
for(const signal of ['SIGINT','SIGTERM']) process.on(signal,()=>{children.forEach(p=>p.kill());process.exit();});
