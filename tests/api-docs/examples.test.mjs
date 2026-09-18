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
