import test from 'node:test';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import {readFileSync} from 'node:fs';
const load = name => import(pathToFileURL(resolve(process.env.EXAMPLE_DIR, `${name}.mjs`)));
const common = await load('README');
const fixture = n => JSON.parse(readFileSync(new URL(`./fixtures/${String(n).padStart(2,'0')}.body`, import.meta.url)));
const optional = async name => { try { return await load(name); } catch (e) { if (e.code === 'ERR_MODULE_NOT_FOUND') return {}; throw e; } };

// Derived from captured row 29, with explicit invoice requirements. Not a settled invoice.
const realTransfer = fixture(29)[0];
const invoice = {from:realTransfer.from, to:realTransfer.to, chainId:1,
  reference:realTransfer.reference, amount:realTransfer.amount};

test('candidate matching rejects false-payment positives and never returns paid', async () => {
  const transfers = await optional('transfers');
  assert.equal(typeof transfers.matchCandidates, 'function', 'Missing candidate-only matcher');
  const match = transfers.matchCandidates;
  assert.equal(match([realTransfer], invoice).status, 'unverified-candidates');
  assert.equal(match([realTransfer, realTransfer], invoice).candidates.length, 1);
  // Extra untrusted token/finality fields never establish settlement.
  assert.equal(match([{...realTransfer,token:'0x'+'f'.repeat(40),receiptStatus:false,confirmations:0}],invoice).status,'unverified-candidates');
  assert.equal(match([{...realTransfer,amount:(BigInt(realTransfer.amount)+1n).toString()}],invoice).status,'unverified-candidates');
  // Synthetic mutations of a captured row, not observed API responses.
  const negatives = [
    {...realTransfer, to:'0x'+'a'.repeat(40)},
    {...realTransfer, from:'0x'+'a'.repeat(40)},
    {...realTransfer, chainId:8453},
    {...realTransfer, reference:realTransfer.reference+' 2'},
    {...realTransfer, reference:realTransfer.reference.toUpperCase()},
    {...realTransfer, targetChain:'4949039107694359620'},
    {...realTransfer, amount:(BigInt(realTransfer.amount)-1n).toString()},
  ];
  for (const row of negatives) assert.equal(match([row], invoice).status, 'no-indexed-match');
  assert.equal(match([], invoice).status, 'no-indexed-match');
  assert.equal(match([realTransfer], {...invoice,to:invoice.to.toUpperCase().replace('0X','0x')}).candidates.length,1);
  for (const bad of [fixture(18), null, {}, [null], [{...realTransfer,amount:1}], [{...realTransfer,chainId:'1'}], [{...realTransfer,txHash:'0x123'}]]) {
    assert.throws(() => match(bad, invoice));
  }
  assert.throws(() => match([realTransfer], {...invoice,amount:'0'}));
});

test('history requests encode exact reference and ISO boundaries; API errors propagate', async () => {
  const transfers = await optional('transfers');
  assert.equal(typeof transfers.historyCandidates, 'function', 'Missing bounded history example');
  let captured;
  const fetchStub = async (url, options) => { captured=url; assert.equal(options.method,'GET'); return {ok:true,json:async()=>fixture(29)}; };
  const special = {...invoice,reference:'Invoice #1 & "test"'};
  const result = await transfers.historyCandidates(special,'2024-01-01T00:00:00.000Z','2025-01-01T00:00:00.000Z',fetchStub);
  assert.equal(captured.searchParams.get('reference'), special.reference);
  assert.equal(captured.searchParams.get('to'), special.to);
  assert.equal(captured.searchParams.get('start'), '2024-01-01T00:00:00.000Z');
  assert.equal(result.complete,false);
  await assert.rejects(transfers.historyCandidates(invoice,'1704067200','1735689600',fetchStub));
  await assert.rejects(transfers.historyCandidates(invoice,'2025-01-01T00:00:00.000Z','2024-01-01T00:00:00.000Z',fetchStub));
  await assert.rejects(transfers.historyCandidates(invoice,'2024-01-01T00:00:00.000Z','2025-01-01T00:00:00.000Z',async()=>({ok:true,json:async()=>fixture(18)})));
});

test('savings selects an explicit module and preserves schema/PPM units', async () => {
  const savings = await optional('savings');
  assert.equal(typeof savings.savingsDisplay,'function','Missing savings schema example');
  const module = '0x27d9ad987bde08a0d083ef7e0e4043c857a17b38';
  const account = realTransfer.from;
  const result = savings.savingsDisplay(fixture(5), fixture(6), 1, module, account);
  assert.equal(result.annualSimplePercent, '3.5');
  assert.equal(result.savedZCHF, '2000000');
  assert.equal(result.collectedInterestZCHF, '11897.690286241121258229');
  for (const rate of [40000,10000,0]) {
    const info=fixture(5); info.status['1'][module].rate=rate;
    assert.equal(savings.savingsDisplay(info,fixture(6),1,module,account).annualSimplePercent,common.formatUnits(String(rate),4));
  }
  for (const badRate of ['35000', '500000000000000000', -1, 1.5, NaN]) {
    const info=fixture(5); info.status['1'][module].rate=badRate;
    assert.throws(()=>savings.savingsDisplay(info,fixture(6),1,module,account));
  }
  assert.throws(()=>savings.savingsDisplay({status:fixture(5)},fixture(6),1,module,account));
  assert.throws(()=>savings.savingsDisplay(fixture(5),{},1,module,account));
  assert.throws(()=>savings.savingsDisplay(fixture(5),fixture(6),1,'0x'+'1'.repeat(40),account));
  const malformed=fixture(6); malformed['1'][module].balance=42;
  assert.throws(()=>savings.savingsDisplay(fixture(5),malformed,1,module,account));
});

test('simple-interest projection applies integer rounding and referral deduction', async () => {
  const savings=await optional('savings');
  assert.equal(typeof savings.estimateSimple,'function','Missing integer projection');
  assert.deepEqual(savings.estimateSimple('10000000000000000000000',40000,31536000,250000,true),
    {gross:'400000000000000000000',fee:'100000000000000000000',net:'300000000000000000000'});
  assert.deepEqual(savings.estimateSimple('150',40000,31536000,250000,true),{gross:'6',fee:'1',net:'5'});
  assert.equal(savings.estimateSimple('150',40000,31536000,250000,false).net,'6');
  assert.equal(savings.estimateSimple('150',40000,0,0,false).gross,'0');
  assert.throws(()=>savings.estimateSimple('1',40000,1,250001,true));
  assert.throws(()=>savings.estimateSimple('1',40000,-1,0,false));
});

test('position owner lookup normalises addresses and validates the map', async () => {
  const prices=await optional('prices');
  assert.equal(typeof prices.ownerPositions,'function','Missing owner lookup');
  assert.equal(prices.ownerPositions(fixture(11),'0x963eC454423CD543dB08bc38fC7B3036B425b301').length,38);
  assert.deepEqual(prices.ownerPositions(fixture(11),'0x'+'1'.repeat(40)),[]);
  assert.throws(()=>prices.ownerPositions({map:null},realTransfer.from));
  assert.throws(()=>prices.ownerPositions({map:{[realTransfer.from]:null}},realTransfer.from));
});

test('valuation uses token decimals and CHF on both sides, with explicit ZCHF conversion', async () => {
  const prices=await optional('prices');
  assert.equal(typeof prices.indicativeRatio,'function','Missing exact-rational valuation');
  // Synthetic fixture: 1.5 tokens, CHF 2/token, debt 1 ZCHF, CHF 1.2/ZCHF.
  const position={collateral:'0x'+'1'.repeat(40),zchf:'0x'+'2'.repeat(40),collateralBalance:'1500000',collateralDecimals:6,minted:'1000000000000000000'};
  const price={address:position.collateral,chainId:1,decimals:6,source:'fixture',timestamp:1000000,price:{chf:2,usd:99}};
  const config={chainId:1,zchfAddress:position.zchf,zchfChf:'1.2',nowMs:1000100,maxAgeMs:1000};
  assert.equal(prices.indicativeRatio(position,price,config).ratioDecimal,'2.5');
  assert.equal(prices.indicativeRatio(position,price,{...config,zchfChf:'1'}).ratioDecimal,'3');
  assert.equal(prices.indicativeRatio({...position,minted:'0'},price,config).status,'no-debt');
  for (const decimals of [0,6,8,18]) {
    const p={...position,collateralDecimals:decimals,collateralBalance:(2n*10n**BigInt(decimals)).toString()};
    assert.equal(prices.indicativeRatio(p,{...price,decimals},config).ratioDecimal,'3.333333');
  }
  const tiny={...price,price:{chf:1e-7,usd:99}};
  assert.equal(prices.indicativeRatio(position,tiny,config).numerator,'15000000000000000000000000');
  for (const bad of [null,{...price,source:null},{...price,timestamp:0},{...price,timestamp:1},{...price,timestamp:2000000},
    {...price,chainId:8453},{...price,address:position.zchf},{...price,price:{usd:99}},{...price,price:{chf:0}},{...price,price:{chf:NaN}}]) {
    assert.throws(()=>prices.indicativeRatio(position,bad,config));
  }
  assert.throws(()=>prices.indicativeRatio({...position,collateralBalance:1},price,config));
  assert.throws(()=>prices.indicativeRatio(position,price,{...config,zchfChf:'0'}));
  assert.throws(()=>prices.indicativeRatio(position,price,{...config,zchfAddress:position.collateral}));
  // Saved live data: at least one nonzero-debt position has an available priced collateral.
  const map=fixture(9); const positions=prices.ownerPositions(fixture(11),realTransfer.from);
  const p=positions.find(p=>BigInt(p.minted)>0n && map[p.collateral.toLowerCase()]?.price.chf>0);
  const q=map[p.collateral.toLowerCase()];
  const result=prices.indicativeRatio(p,q,{chainId:q.chainId,zchfAddress:p.zchf,zchfChf:'1',nowMs:q.timestamp,maxAgeMs:1000});
  assert.equal(result.status,'indicative');
  assert.ok(BigInt(result.denominator)>0n);
});

test('raw integer formatting preserves fractional and large values', () => {
  assert.equal(common.formatUnits('1500000000000000000', 18), '1.5');
  assert.equal(common.formatUnits('123456789012345678901234567890', 18), '123456789012.34567890123456789');
  assert.equal(common.formatUnits('123', 0), '123');
  assert.equal(common.formatUnits('1000001', 6), '1.000001');
  assert.equal(common.formatUnits('1', 8), '0.00000001');
  for (const bad of ['-1','1e18','1.2','',null,1,1.5]) {
    assert.throws(() => common.formatUnits(bad, 18));
  }
  assert.throws(() => common.formatUnits('1', -1));
});

test('HTTP failures, invalid JSON and error envelopes reject', async () => {
  const stub = (body, ok=true) => async () => ({ok, status: ok ? 200 : 503, json: async () => body});
  assert.deepEqual(await common.getJson('/status', stub({api: {status: 'healthy'}})), {api: {status: 'healthy'}});
  for (const body of [null, {error:'ApolloError'}, {errors:[]}, {statusCode:500}]) {
    await assert.rejects(common.getJson('/status', stub(body)));
  }
  await assert.rejects(common.getJson('/status', stub([], false)));
  await assert.rejects(common.getJson('/status', async () => ({ok:true, json:async () => {throw Error('bad JSON');}})));
  await assert.rejects(common.getJson('https://example.org', stub({})));
});
