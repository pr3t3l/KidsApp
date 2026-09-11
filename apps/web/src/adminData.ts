import { apiRequest, DEMO_MODE } from "./api";
import { requirePassedProviderHealth, type ProviderHealthResult } from "./providerConfig";

export const ADMIN_NOTICE_EVENT = "kids:admin-notice";
export type AdminNotice = { messageKey:string; subject:string; at?:string };

function announceAdminNotice(notice:AdminNotice):void {
  if(typeof window!=="undefined")window.dispatchEvent(new CustomEvent<AdminNotice>(ADMIN_NOTICE_EVENT,{detail:notice}));
}

export type AdminRole = "platform_owner" | "editorial_specialist" | "support_operator";
export type AdminSection = "overview" | "coverage" | "activities" | "create" | "reviews" | "pilots" | "feedback" | "ai" | "providers" | "people" | "incidents" | "audit" | "settings";

export type CoverageCell = { cellId: string; area: string; ageBand: string; eligibleCount: number; effectiveCoverage: number; target: number; mechanisms: string[]; gapType: string };
export type CatalogGap = { gapId: string; type: string; priority: number; reason: string; cell: CoverageCell; nearMisses: Array<{activityVersionId:string; reasons:string[]}>; demand: {status:string}; quality:{status:string} };
export type CoverageTarget = {targetId:string;version:number;cellId:string;area:string;ageBand:string;targetValue:number;effectiveFrom:string};
export type ActiveRoute = { policyId:string; primaryDeploymentId:string; fallbackDeploymentIds:string[]; state:string; environment:string; maxOutputTokens:number; timeoutMs:number; testStatus:string; evalStatus:string;allowedUpstreams?:string[];temperature?:number;reasoningEffort?:string;maxEstimatedUsd?:number|null;allowedDataClasses?:string[];allowedLocales?:string[];canaryPercent?:number;promptVersion?:string;schemaVersion?:string };
export type RouteRow = { operation: { operationKey:string; endpoint:string; stage:string; capability:string; description:string; usesAi:boolean; allowedDataClasses?:string[]; allowedLocales?:string[] }; activeRoute: null | ActiveRoute };
export type RouteDraft={environment:string;primaryDeploymentId:string;fallbackDeploymentIds:string[];allowedUpstreams:string[];temperature:number;reasoningEffort:string;maxOutputTokens:number;timeoutMs:number;maxEstimatedUsd:number|null;canaryPercent:number};
export type ProviderConnection = { connectionId:string; name:string; provider:string; baseUrl:string; secretLastFour:string; state:string; lastCheckedAt?:string|null };
export type Deployment = { deploymentId:string; connectionId:string; provider:string; modelId:string; capabilities:string[]; state:string };
export type RateCard = {rateId:string;deploymentId:string;version:number;currency:string;inputPerMillion:number;cachedInputPerMillion:number;cacheWritePerMillion:number;outputPerMillion:number;reasoningPerMillion:number;embeddingPerMillion:number;imagePerUnit:number;audioPerMinute:number;toolPerCall:number;sourceUrl:string;effectiveFrom:string;verifiedAt:string};
export type Budget = {budgetId:string;scopeType:string;scopeKey:string;period:string;limitUsd:number;warnPercent?:number;pausePercent?:number;stopPercent?:number;spentUsd:number;state:string};
export type EditorialSource = {sourceId:string;url:string;title:string;licenseCode:string;licenseUrl?:string|null;exactResourceVerified:boolean;disposition:string};
export type EditorialReview = {gate:string;decision:"approve"|"return"|"block";independent:boolean;reviewerRole?:AdminRole;reviewerId?:string;recordedAt?:string;findings?:string[]};
export type MachineFinding = string | {gate?:string;severity?:string;message?:string;code?:string};
export type EditorialJob = { jobId:string; gapId:string; activityVersionId?:string; contentHash?:string; indexState?:string; state:string; stage:string; stageIndex?:number; updatedAt:string; brief?:{primaryArea?:string;ageBand?:string;[key:string]:unknown}; sources?:EditorialSource[]; reviews?:EditorialReview[]; machineFindings?:MachineFinding[]; artifacts?:Record<string,unknown>; pilot?:Record<string,unknown>|null; release?:Record<string,unknown>|null };
export type PilotCohort = {cohortId:string;name:string;state:"draft"|"active"|"closed";startsAt?:string|null;endsAt?:string|null;familyIds:string[];activityVersionIds:string[];createdAt:string};
export type ResearchResult = {url:string;title:string;description:string;licenseVerified:boolean;transient:boolean};
export type AdminPerson = {assignmentId:string;userId:string;role:AdminRole;assignedDomains:string[];active:boolean;createdAt:string;maskedEmail?:string;delivery?:string};
export type ReviewAssignment = {assignmentId:string;jobId?:string;activityVersionId:string;gate:string;reviewerId:string;required:boolean;independent:boolean;dueAt?:string|null;createdAt:string};
export type FamilyFeedback = {feedbackId:string;familyRef:string;useful:boolean|null;category:string;comment?:string|null;screen:string;activityVersionId?:string|null;sessionId?:string|null;appVersion:string;locale:string;journeyState?:string|null;incidentId?:string|null;deleteAfter:string;createdAt:string};
export type ContentIncident = {incidentId:string;activityVersionId?:string|null;familyRef?:string|null;feedbackId?:string|null;severity:string;category:string;summary:string;state:string;openedAt:string;resolvedAt?:string|null};
export type AuditEvent = {auditEventId:string;actorUserId?:string|null;actorRole:string;eventType:string;resourceType:string;resourceId:string;reason?:string|null;detail:Record<string,unknown>;createdAt:string};
export type AdminActivity = {activityVersionId:string;title:string;primaryArea:string;age:[number,number];risk:string;status:string;releaseChannel:string;contentHash:string;localeState?:string};
export type ProductSettings = {settingVersionId:string;version:number;brand:string;locales:Array<"en-US"|"es-US">;timeZone:string;guardrails:Record<string,boolean>;active:boolean;createdAt:string};

const areas = ["physics","engineering","electricity","mathematics","safe_chemistry","biology_nature","motor_skills","creativity","logical_thinking","communication","self_regulation","practical_life"];
const labels: Record<string,string> = { physics:"Física", engineering:"Ingeniería", electricity:"Electricidad", mathematics:"Matemáticas", safe_chemistry:"Química segura", biology_nature:"Biología y naturaleza", motor_skills:"Motricidad", creativity:"Creatividad", logical_thinking:"Pensamiento lógico", communication:"Comunicación", self_regulation:"Autorregulación", practical_life:"Vida práctica" };
export const areaLabel = (area:string) => labels[area] ?? area;

const demoCells: CoverageCell[] = areas.flatMap((area, areaIndex) => ["5-6","7-8","9-10"].map((ageBand, ageIndex) => {
  const covered = !["safe_chemistry", "mathematics", "communication", "self_regulation", "motor_skills"].includes(area) && (areaIndex + ageIndex) % 3 !== 0;
  const partial = !covered && ["mathematics", "communication", "self_regulation", "motor_skills"].includes(area);
  const score = covered ? 1 : partial ? .5 : 0;
  return { cellId:`${area}:${ageBand}`, area, ageBand, eligibleCount:score ? 1 : 0, effectiveCoverage:score, target:1, mechanisms:score ? [`${area}-mechanism`] : [], gapType:score === 1 ? "none" : score === 0 ? "absolute" : "coverage" };
}));
const demoGaps: CatalogGap[] = demoCells.filter(cell => cell.gapType !== "none").map(cell => ({ gapId:cell.cellId, type:cell.gapType, priority:cell.effectiveCoverage ? .25 : .5, reason:cell.effectiveCoverage ? `La cobertura efectiva es ${cell.effectiveCoverage} de ${cell.target}.` : `No existe una actividad elegible de ${areaLabel(cell.area)} para ${cell.ageBand} años.`, cell, nearMisses:[], demand:{status:"insufficient_data"}, quality:{status:"insufficient_data"} }));

const operationNames = [
  ["companion.classify","/v1/companion/interactions","classify","OpenRouter","openai/gpt-4.1-mini"],
  ["companion.answer","/v1/companion/interactions","answer","OpenRouter","anthropic/claude-sonnet-4"],
  ["plan.explain","/v1/plans/{id}","explain","OpenRouter","openai/gpt-4.1-mini"],
  ["catalog.rewrite_query","/v1/catalog/search","rewrite","OpenRouter","openai/gpt-4.1-mini"],
  ["retrieval.embed","internal","embed","OpenAI","text-embedding-3-small"],
  ["activity.ideate","/v1/editorial/jobs","idea","OpenRouter","google/gemini-2.5-pro"],
  ["activity.author.core","/v1/editorial/jobs","core","Anthropic","claude-sonnet-4-5"],
  ["activity.review.education","/v1/editorial/reviews","education","OpenRouter","openai/gpt-4.1"],
  ["activity.review.subject","/v1/editorial/reviews","subject","OpenRouter","google/gemini-2.5-pro"],
  ["activity.review.safety","/v1/editorial/reviews","safety","Anthropic","claude-sonnet-4-5"],
  ["activity.localize","/v1/editorial/jobs","localize","OpenAI","gpt-4.1-mini"],
  ["feedback.redact","/v1/feedback","redact","OpenAI","gpt-4.1-mini"],
  ["family.session.start","/v1/sessions","start","—","No usa IA"],
  ["editorial.release","/v1/editorial/releases","release","—","No usa IA"],
] as const;

const demoRoutes: RouteRow[] = operationNames.map(([key,endpoint,stage,provider,model], index) => ({
  operation:{operationKey:key,endpoint,stage,capability:model === "No usa IA" ? "deterministic" : key === "retrieval.embed" ? "embedding" : "structured_text",description:"Ruta versionada y auditable.",usesAi:model !== "No usa IA"},
  activeRoute:model === "No usa IA" ? null : {policyId:`route-${index}`,primaryDeploymentId:`${provider}|${model}`,fallbackDeploymentIds:[],state:"active",environment:"development",maxOutputTokens:key.startsWith("companion")?350:2000,timeoutMs:12000,testStatus:"passed",evalStatus:"passed"}
}));

const demoConnections: ProviderConnection[] = [
  {connectionId:"openrouter-default",name:"OpenRouter principal",provider:"openrouter",baseUrl:"https://openrouter.ai/api/v1",secretLastFour:"••••",state:"active",lastCheckedAt:new Date().toISOString()},
  {connectionId:"openai-direct",name:"OpenAI directo",provider:"openai",baseUrl:"https://api.openai.com/v1",secretLastFour:"—",state:"disabled"},
  {connectionId:"anthropic-direct",name:"Anthropic directo",provider:"anthropic",baseUrl:"https://api.anthropic.com/v1",secretLastFour:"—",state:"disabled"},
];

const demoDeployments: Deployment[] = [
  {deploymentId:"or-sonnet",connectionId:"openrouter-default",provider:"openrouter",modelId:"anthropic/claude-sonnet-4",capabilities:["structured_text"],state:"active"},
  {deploymentId:"or-gpt-mini",connectionId:"openrouter-default",provider:"openrouter",modelId:"openai/gpt-4.1-mini",capabilities:["structured_text"],state:"active"},
  {deploymentId:"or-gemini",connectionId:"openrouter-default",provider:"openrouter",modelId:"google/gemini-2.5-pro",capabilities:["structured_text"],state:"approved"},
];

export type AdminData = {
  coverage:{overview:{catalogActivities:number;eligibleActivities:number;gaps:number;ageCoverage:Record<string,number>};cells:CoverageCell[];gaps:CatalogGap[];areaCounts:Array<{area:string;primary:number;secondary:number}>;blocked:Array<{activityVersionId:string;reasons:string[]}>;targetRecords:CoverageTarget[]};
  routes:RouteRow[]; connections:ProviderConnection[]; deployments:Deployment[];
  costs:{summary:{displayUsd:number;calls:number;inputTokens:number;outputTokens:number;latencyP50Ms:number;latencyP95Ms:number;fallbacks:number;errors:number;costSource:string;uniqueAdults:number;uniqueFamilies:number;costPerCallUsd:number;costPerFamilyUsd:number};budgets:Budget[];rates:RateCard[]};
  jobs:EditorialJob[]; cohorts:PilotCohort[]; activities:AdminActivity[]; people:AdminPerson[]; reviewAssignments:ReviewAssignment[]; feedback:FamilyFeedback[]; incidents:ContentIncident[]; auditEvents:AuditEvent[]; settings:ProductSettings;
};
export type AdminIdentity = {userId:string;roles:AdminRole[];mfa:boolean};

export const demoAdminData: AdminData = {
  coverage:{overview:{catalogActivities:13,eligibleActivities:12,gaps:demoGaps.length,ageCoverage:{"5-6":9,"7-8":12,"9-10":12}},cells:demoCells,gaps:demoGaps,areaCounts:areas.map(area=>({area,primary:["engineering","physics","electricity"].includes(area)?2:["mathematics","self_regulation"].includes(area)?0:1,secondary:2})),blocked:[{activityVersionId:"ACT-0003@1.0.0",reasons:["independent_specialist_required"]},{activityVersionId:"ACT-0011@1.0.0",reasons:["founder_execution_required"]},{activityVersionId:"ACT-0012@1.0.0",reasons:["founder_execution_required"]},{activityVersionId:"ACT-0013@1.0.0",reasons:["founder_execution_required"]}],targetRecords:[]},
  routes:demoRoutes,connections:demoConnections,deployments:demoDeployments,
  costs:{summary:{displayUsd:0,calls:0,inputTokens:0,outputTokens:0,latencyP50Ms:0,latencyP95Ms:0,fallbacks:0,errors:0,costSource:"none",uniqueAdults:0,uniqueFamilies:0,costPerCallUsd:0,costPerFamilyUsd:0},budgets:[{budgetId:"global",scopeType:"global",scopeKey:"all",period:"month",limitUsd:15,warnPercent:80,pausePercent:95,stopPercent:100,spentUsd:0,state:"ok"}],rates:[]},jobs:[],cohorts:[],activities:[{activityVersionId:"ACT-0001@1.0.0",title:"Paper Bridge",primaryArea:"engineering",age:[5,10],risk:"A",status:"published",releaseChannel:"production",contentHash:"demo:ACT-0001"},{activityVersionId:"ACT-0002@1.0.0",title:"Seed Sorter",primaryArea:"logical_thinking",age:[5,10],risk:"A",status:"published",releaseChannel:"production",contentHash:"demo:ACT-0002"},{activityVersionId:"ACT-0003@1.0.0",title:"Conductivity Tester",primaryArea:"electricity",age:[8,10],risk:"C",status:"review",releaseChannel:"unreleased",contentHash:"demo:ACT-0003"}],people:[{assignmentId:"owner",userId:"00000000-0000-0000-0000-000000000001",role:"platform_owner",assignedDomains:[],active:true,createdAt:new Date().toISOString()}],reviewAssignments:[],feedback:[],incidents:[],auditEvents:[],settings:{settingVersionId:"demo-settings",version:1,brand:"Kids Learning System",locales:["es-US","en-US"],timeZone:"America/New_York",guardrails:{childAccounts:false,voice:false,photos:false,community:false,inAppPayments:false},active:true,createdAt:new Date().toISOString()}
};

export async function loadAdminIdentity(previewRole:AdminRole="platform_owner"): Promise<AdminIdentity> {
  if (DEMO_MODE) return {userId:"00000000-0000-0000-0000-000000000001",roles:[previewRole],mfa:true};
  return apiRequest<AdminIdentity>("/v1/admin/me");
}

export async function loadAdminData(role:AdminRole="platform_owner"): Promise<AdminData> {
  if (DEMO_MODE) return structuredClone(demoAdminData);
  if (role === "editorial_specialist") {
    const [coverage,jobs,reviewAssignments,incidents,activities] = await Promise.all([
      apiRequest<AdminData["coverage"]>("/v1/admin/catalog/coverage"),
      apiRequest<EditorialJob[]>("/v1/editorial/jobs"),
      apiRequest<ReviewAssignment[]>("/v1/admin/review-assignments"),
      apiRequest<ContentIncident[]>("/v1/admin/incidents"),
      apiRequest<AdminActivity[]>("/v1/admin/catalog/activities"),
    ]);
    return {...structuredClone(demoAdminData),coverage,jobs,reviewAssignments,incidents,activities,routes:[],connections:[],deployments:[],costs:structuredClone(demoAdminData.costs),cohorts:[],people:[],feedback:[],auditEvents:[]};
  }
  if (role === "support_operator") {
    const [cohorts,feedback,incidents]=await Promise.all([apiRequest<PilotCohort[]>("/v1/editorial/pilot-cohorts"),apiRequest<FamilyFeedback[]>("/v1/admin/family-feedback"),apiRequest<ContentIncident[]>("/v1/admin/incidents")]);
    return {...structuredClone(demoAdminData),routes:[],connections:[],deployments:[],jobs:[],costs:structuredClone(demoAdminData.costs),cohorts,feedback,incidents,people:[],reviewAssignments:[],auditEvents:[]};
  }
  const [coverage,routes,connections,deployments,costs,jobs,cohorts,activities,people,reviewAssignments,feedback,incidents,auditEvents,settings] = await Promise.all([
    apiRequest<AdminData["coverage"]>("/v1/admin/catalog/coverage"),
    apiRequest<RouteRow[]>("/v1/admin/ai/operations"),
    apiRequest<ProviderConnection[]>("/v1/admin/ai/connections"),
    apiRequest<Deployment[]>("/v1/admin/ai/deployments"),
    apiRequest<AdminData["costs"]>("/v1/admin/ai/costs"),
    apiRequest<EditorialJob[]>("/v1/editorial/jobs"),
    apiRequest<PilotCohort[]>("/v1/editorial/pilot-cohorts"),
    apiRequest<AdminActivity[]>("/v1/admin/catalog/activities"),
    apiRequest<AdminPerson[]>("/v1/admin/people"),
    apiRequest<ReviewAssignment[]>("/v1/admin/review-assignments"),
    apiRequest<FamilyFeedback[]>("/v1/admin/family-feedback"),
    apiRequest<ContentIncident[]>("/v1/admin/incidents"),
    apiRequest<AuditEvent[]>("/v1/admin/audit"),
    apiRequest<ProductSettings>("/v1/admin/settings"),
  ]);
  return {coverage,routes,connections,deployments,costs,jobs,cohorts,activities,people,reviewAssignments,feedback,incidents,auditEvents,settings};
}

export async function updateCoverageTarget(area:string,ageBand:string,targetValue:number):Promise<AdminData["coverage"]>{
  if(DEMO_MODE){
    const record:CoverageTarget={targetId:crypto.randomUUID(),version:(demoAdminData.coverage.targetRecords.at(-1)?.version??0)+1,cellId:`${area}:${ageBand}`,area,ageBand,targetValue,effectiveFrom:new Date().toISOString()};
    demoAdminData.coverage.targetRecords.push(record);
    demoAdminData.coverage.cells=demoAdminData.coverage.cells.map(cell=>cell.cellId===record.cellId?{...cell,target:targetValue,gapType:cell.effectiveCoverage>=targetValue?"none":cell.effectiveCoverage?"coverage":"absolute"}:cell);
    const changed=demoAdminData.coverage.cells.find(cell=>cell.cellId===record.cellId)!;
    demoAdminData.coverage.gaps=demoAdminData.coverage.gaps.filter(gap=>gap.gapId!==record.cellId);
    if(changed.gapType!=="none")demoAdminData.coverage.gaps.push({gapId:record.cellId,type:changed.gapType,priority:Math.max(0,1-changed.effectiveCoverage/targetValue)*.5,reason:`La cobertura efectiva es ${changed.effectiveCoverage.toFixed(2)} de ${targetValue.toFixed(2)}.`,cell:changed,nearMisses:[],demand:{status:"insufficient_data"},quality:{status:"insufficient_data"}});
    demoAdminData.coverage.overview.gaps=demoAdminData.coverage.gaps.length;
    return structuredClone(demoAdminData.coverage);
  }
  await apiRequest<CoverageTarget>("/v1/admin/catalog/coverage-targets",{method:"POST",body:JSON.stringify({area,ageBand,targetValue})});
  return apiRequest<AdminData["coverage"]>("/v1/admin/catalog/coverage");
}

export async function inviteAdmin(input:{email:string;role:"editorial_specialist"|"support_operator";assignedDomains:string[]}):Promise<AdminPerson>{
  if(DEMO_MODE)return {assignmentId:crypto.randomUUID(),userId:crypto.randomUUID(),role:input.role,assignedDomains:input.assignedDomains,active:true,createdAt:new Date().toISOString(),maskedEmail:`${input.email[0]}***@${input.email.split("@")[1]}`,delivery:"simulated"};
  return apiRequest<AdminPerson>("/v1/admin/people/invitations",{method:"POST",body:JSON.stringify(input)});
}

export async function inviteFamilyTester(email:string):Promise<{invitationId:string;userId:string;delivery:string;maskedEmail:string;createdAt:string}>{
  if(DEMO_MODE)return {invitationId:crypto.randomUUID(),userId:crypto.randomUUID(),delivery:"simulated",maskedEmail:`${email[0]}***@${email.split("@")[1]}`,createdAt:new Date().toISOString()};
  return apiRequest("/v1/admin/family-invitations",{method:"POST",body:JSON.stringify({email})});
}

export async function updateAdminPerson(person:AdminPerson,input:{assignedDomains:string[];active:boolean}):Promise<AdminPerson>{
  if(DEMO_MODE)return {...person,...input};
  return apiRequest<AdminPerson>(`/v1/admin/people/${person.assignmentId}`,{method:"PUT",body:JSON.stringify(input)});
}

export async function createSupportGrant(input:{supportUserId:string;familyId:string;purpose:string;expiresAt:string}):Promise<Record<string,unknown>>{
  if(DEMO_MODE)return {grantId:crypto.randomUUID(),...input,familyRef:`fam-demo`,createdAt:new Date().toISOString()};
  return apiRequest("/v1/admin/support-grants",{method:"POST",body:JSON.stringify(input)});
}

export async function assignReview(input:{jobId:string;gate:string;reviewerId:string;dueAt?:string|null}):Promise<ReviewAssignment>{
  if(DEMO_MODE){const job=demoAdminData.jobs.find(item=>item.jobId===input.jobId);return {assignmentId:crypto.randomUUID(),jobId:input.jobId,activityVersionId:job?.activityVersionId??"demo@0.1.0",gate:input.gate,reviewerId:input.reviewerId,required:true,independent:true,dueAt:input.dueAt,createdAt:new Date().toISOString()};}
  return apiRequest<ReviewAssignment>("/v1/admin/review-assignments",{method:"POST",body:JSON.stringify(input)});
}

export async function updateIncident(incident:ContentIncident,state:"contained"|"investigating"|"resolved",reason:string):Promise<ContentIncident>{
  if(DEMO_MODE)return {...incident,state,resolvedAt:state==="resolved"?new Date().toISOString():null};
  return apiRequest<ContentIncident>(`/v1/admin/incidents/${incident.incidentId}/state`,{method:"POST",body:JSON.stringify({state,reason})});
}

export async function updateProductSettings(input:{brand:string;locales:Array<"en-US"|"es-US">;timeZone:string}):Promise<ProductSettings>{
  if(DEMO_MODE)return {...demoAdminData.settings,...input,settingVersionId:crypto.randomUUID(),version:demoAdminData.settings.version+1,createdAt:new Date().toISOString()};
  return apiRequest<ProductSettings>("/v1/admin/settings",{method:"PUT",body:JSON.stringify(input)});
}

export async function createProvider(input:{name:string;provider:string;apiKey:string;baseUrl:string}): Promise<ProviderConnection> {
  if (DEMO_MODE) return {connectionId:crypto.randomUUID(),name:input.name,provider:input.provider,baseUrl:input.baseUrl,secretLastFour:input.apiKey.slice(-4),state:"active"};
  return apiRequest<ProviderConnection>("/v1/admin/ai/connections",{method:"POST",body:JSON.stringify(input)});
}

export async function testProvider(connection:ProviderConnection):Promise<ProviderConnection>{
  if(DEMO_MODE){const checkedAt=new Date().toISOString();announceAdminNotice({messageKey:"Conexión verificada",subject:connection.name,at:checkedAt});return {...connection,state:"active",lastCheckedAt:checkedAt};}
  const result=await apiRequest<ProviderHealthResult>(`/v1/admin/ai/connections/${connection.connectionId}/test`,{method:"POST"});
  const checkedAt=requirePassedProviderHealth(result);
  announceAdminNotice({messageKey:"Conexión verificada",subject:connection.name,at:checkedAt});
  return {...connection,lastCheckedAt:checkedAt};
}

export async function rotateProvider(connection:ProviderConnection,apiKey:string):Promise<ProviderConnection>{
  if(DEMO_MODE)return {...connection,secretLastFour:apiKey.slice(-4),state:"active"};
  return apiRequest<ProviderConnection>(`/v1/admin/ai/connections/${connection.connectionId}/rotate`,{method:"POST",body:JSON.stringify({apiKey})});
}

export async function revokeProvider(connection:ProviderConnection):Promise<ProviderConnection>{
  if(DEMO_MODE)return {...connection,state:"revoked"};
  return apiRequest<ProviderConnection>(`/v1/admin/ai/connections/${connection.connectionId}/revoke`,{method:"POST"});
}

export async function createDeployment(input:{connectionId:string;modelId:string;capabilities:string[];dataClasses:string[];locales:Array<"en-US"|"es-US">}):Promise<Deployment>{
  if(DEMO_MODE){const provider=demoConnections.find(item=>item.connectionId===input.connectionId)?.provider??"openrouter";return {deploymentId:crypto.randomUUID(),connectionId:input.connectionId,provider,modelId:input.modelId,capabilities:input.capabilities,state:"candidate"};}
  return apiRequest<Deployment>("/v1/admin/ai/deployments",{method:"POST",body:JSON.stringify(input)});
}

export async function createRate(input:Omit<RateCard,"rateId"|"version"|"verifiedAt">):Promise<RateCard>{
  if(DEMO_MODE)return {...input,rateId:crypto.randomUUID(),version:1,verifiedAt:new Date().toISOString()};
  return apiRequest<RateCard>("/v1/admin/ai/prices",{method:"POST",body:JSON.stringify(input)});
}

export async function createBudget(input:{scopeType:string;scopeKey:string;period:string;limitUsd:number;warnPercent:number;pausePercent:number;stopPercent:number}):Promise<Budget>{
  if(DEMO_MODE)return {...input,budgetId:crypto.randomUUID(),spentUsd:0,state:"ok"};
  return apiRequest<Budget>("/v1/admin/ai/budgets",{method:"POST",body:JSON.stringify(input)});
}

export async function loadUsage(filters:{operationKey?:string;provider?:string;model?:string;environment?:string;locale?:string}):Promise<AdminData["costs"]["summary"]>{
  if(DEMO_MODE)return structuredClone(demoAdminData.costs.summary);
  const query=new URLSearchParams();Object.entries(filters).forEach(([key,value])=>{if(value)query.set(key,value)});
  return apiRequest<AdminData["costs"]["summary"]>(`/v1/admin/ai/usage?${query.toString()}`);
}

export async function createJob(gapId:string): Promise<EditorialJob> {
  if (DEMO_MODE) return {jobId:crypto.randomUUID(),gapId,state:"draft",stage:"research",stageIndex:0,updatedAt:new Date().toISOString(),sources:[],reviews:[],pilot:null,release:null};
  return apiRequest<EditorialJob>("/v1/editorial/jobs",{method:"POST",body:JSON.stringify({gapId,notes:"Created from the catalog coverage workspace"})});
}

export async function researchSources(query:string): Promise<{results:ResearchResult[];rightsNotice:string}> {
  if (DEMO_MODE) return {results:[
    {url:"https://www.nasa.gov/stem-content/",title:"NASA STEM resources",description:"Candidate public learning reference; exact page and reuse terms still require verification.",licenseVerified:false,transient:true},
    {url:"https://www.si.edu/educators",title:"Smithsonian educator resources",description:"Candidate educator reference; discovery is not permission to reuse expression.",licenseVerified:false,transient:true},
  ],rightsNotice:"Encontrar una página no verifica ni concede derechos de reutilización."};
  return apiRequest(`/v1/editorial/research?query=${encodeURIComponent(query)}&locale=es-US`);
}

export async function addJobSource(jobId:string,input:{url:string;title:string;licenseCode:string;licenseUrl?:string;exactResourceVerified:boolean}):Promise<EditorialSource>{
  if(DEMO_MODE){const code=input.licenseCode.toUpperCase().replaceAll("-","_").replaceAll(" ","_");const allowed=["CC0","PUBLIC_DOMAIN","CC_BY"].includes(code);return {sourceId:crypto.randomUUID(),...input,licenseCode:code,disposition:!input.exactResourceVerified?"needs_verification":allowed?"eligible":"manual_rights_review"}}
  return apiRequest(`/v1/editorial/jobs/${jobId}/sources`,{method:"POST",body:JSON.stringify(input)});
}

const editorialStages=["research","idea","core","materials_safety","steps","roles_adaptations","closeout","localize","human_review"];
export async function advanceJob(job:EditorialJob):Promise<EditorialJob>{
  if(DEMO_MODE){if(job.stage==="research"&&!job.sources?.some(source=>source.disposition==="eligible"))throw new Error("Añade al menos una fuente exacta con derechos elegibles.");const index=Math.max(0,editorialStages.indexOf(job.stage));const stage=editorialStages[Math.min(editorialStages.length-1,index+1)];return {...job,stage,stageIndex:index+1,state:stage==="human_review"?"review":"draft",updatedAt:new Date().toISOString()}}
  return apiRequest(`/v1/editorial/jobs/${job.jobId}/advance`,{method:"POST"});
}

export async function reindexJob(job:EditorialJob):Promise<EditorialJob>{
  if(DEMO_MODE)return {...job,indexState:"complete",updatedAt:new Date().toISOString()};
  await apiRequest(`/v1/editorial/jobs/${job.jobId}/reindex`,{method:"POST"});
  return apiRequest<EditorialJob>(`/v1/editorial/jobs/${job.jobId}`);
}

export async function reviewJob(job:EditorialJob,input:{gate:string;decision:"approve"|"return"|"block";findings:string[];independent:boolean;reviewerRole:AdminRole}):Promise<EditorialJob>{
  if(DEMO_MODE){
    const review={...input,recordedAt:new Date().toISOString()};
    const reviews=[...(job.reviews??[]),review];
    const required=["education","subject","safety","language","rights"];
    const ready=required.every(name=>reviews.some(item=>item.gate===name&&item.decision==="approve"));
    const needsRevision=input.decision!=="approve";
    return {...job,reviews,state:needsRevision?"revision":ready?"ready_for_pilot":job.state,stage:ready?"ready_for_pilot":job.stage,updatedAt:new Date().toISOString()};
  }
  await apiRequest(`/v1/editorial/jobs/${job.jobId}/reviews`,{method:"POST",body:JSON.stringify({gate:input.gate,decision:input.decision,independent:input.independent,findings:input.findings})});
  return apiRequest(`/v1/editorial/jobs/${job.jobId}`);
}

export async function pilotJob(job:EditorialJob,input:{cohort:string;startedSessions:number;completedSessions:number;usefulPercent:number;durationFitPercent:number;criticalIncidents:number}):Promise<EditorialJob>{
  if(DEMO_MODE)return {...job,state:"family_pilot",pilot:input,updatedAt:new Date().toISOString()};
  await apiRequest(`/v1/editorial/jobs/${job.jobId}/pilots`,{method:"POST",body:JSON.stringify(input)});
  return apiRequest(`/v1/editorial/jobs/${job.jobId}`);
}

export async function releaseJob(job:EditorialJob,channel:"family_pilot"|"production"):Promise<EditorialJob>{
  if(DEMO_MODE){if(channel==="production"&&!job.reviews?.some(item=>item.reviewerRole==="editorial_specialist"&&["education","subject"].includes(item.gate)))throw new Error("Falta una revisión profesional independiente.");return {...job,state:channel==="production"?"published":"family_pilot",release:{channel,machineApproved:false},updatedAt:new Date().toISOString()};}
  await apiRequest(`/v1/editorial/jobs/${job.jobId}/release?channel=${channel}`,{method:"POST"});
  return apiRequest(`/v1/editorial/jobs/${job.jobId}`);
}

export async function createPilotCohort(name:string):Promise<PilotCohort>{
  if(DEMO_MODE)return {cohortId:crypto.randomUUID(),name,state:"draft",familyIds:[],activityVersionIds:[],createdAt:new Date().toISOString()};
  return apiRequest<PilotCohort>("/v1/editorial/pilot-cohorts",{method:"POST",body:JSON.stringify({name})});
}

export async function addPilotFamily(cohort:PilotCohort,familyId:string):Promise<PilotCohort>{
  if(DEMO_MODE)return {...cohort,familyIds:Array.from(new Set([...cohort.familyIds,familyId]))};
  return apiRequest<PilotCohort>(`/v1/editorial/pilot-cohorts/${cohort.cohortId}/families`,{method:"POST",body:JSON.stringify({familyId})});
}

export async function addPilotActivity(cohort:PilotCohort,activityVersionId:string):Promise<PilotCohort>{
  if(DEMO_MODE)return {...cohort,activityVersionIds:Array.from(new Set([...cohort.activityVersionIds,activityVersionId]))};
  return apiRequest<PilotCohort>(`/v1/editorial/pilot-cohorts/${cohort.cohortId}/activities`,{method:"POST",body:JSON.stringify({activityVersionId})});
}

export async function activatePilotCohort(cohort:PilotCohort):Promise<PilotCohort>{
  if(DEMO_MODE){if(!cohort.familyIds.length||!cohort.activityVersionIds.length)throw new Error("Añade una familia y una versión exacta.");return {...cohort,state:"active"};}
  return apiRequest<PilotCohort>(`/v1/editorial/pilot-cohorts/${cohort.cohortId}/activate`,{method:"POST"});
}

export async function activateRoute(row:RouteRow,draft:RouteDraft): Promise<RouteRow> {
  if (!row.operation.usesAi) return row;
  if (DEMO_MODE) return {...row,activeRoute:{...(row.activeRoute ?? {policyId:crypto.randomUUID(),state:"active",testStatus:"passed",evalStatus:"passed"}),...draft,policyId:crypto.randomUUID(),state:"active",testStatus:"passed",evalStatus:"passed"}};
  const policy = await apiRequest<{policyId:string}>(`/v1/admin/ai/operations/${row.operation.operationKey}/routing`,{
    method:"PUT",
    body:JSON.stringify({
      ...draft,fallbackDeploymentIds:draft.fallbackDeploymentIds.filter(id=>id!==draft.primaryDeploymentId),allowedDataClasses:row.operation.allowedDataClasses ?? ["published_activity"],
      allowedLocales:row.operation.allowedLocales ?? ["en-US","es-US"],
      promptVersion:`${row.operation.operationKey}@1`,schemaVersion:"operation@1"
    })
  });
  const suffix = `?policy_id=${encodeURIComponent(policy.policyId)}`;
  await apiRequest(`/v1/admin/ai/operations/${row.operation.operationKey}/test${suffix}`,{method:"POST"});
  await apiRequest(`/v1/admin/ai/operations/${row.operation.operationKey}/evaluate${suffix}`,{method:"POST"});
  const activeRoute = await apiRequest<RouteRow["activeRoute"]>(`/v1/admin/ai/operations/${row.operation.operationKey}/activate${suffix}`,{method:"POST"});
  return {...row,activeRoute};
}
