import ROOT
from array import array

ROOT.gROOT.SetBatch(1)
f = ROOT.TFile("filename.root")
t = f.Get("thedata")

nentries = t.GetEntries()
print nentries
r = ROOT.TTreeReader(t)
px = []
py = []
pz = []
fout = ROOT.TFile("varfilename.root", "RECREATE")
et = []
pt = []
phi = []
pTtag = {1:"_softestParticle", 2:"_softParticle", 3:"_hardParticle", 4:"_hardestParticle"}
for i in range(4):
  px.append(ROOT.TTreeReaderValue(float)(r,'px%i'%(i+1)))
  py.append(ROOT.TTreeReaderValue(float)(r,'py%i'%(i+1)))
  pz.append(ROOT.TTreeReaderValue(float)(r,'pz%i'%(i+1)))
  et.append(ROOT.TH1F('heta%s'%(pTtag[i+1]), 'eta%s'%(pTtag[i+1]), 40, -3, 3))
  pt.append(ROOT.TH1F('hpT%s'%(pTtag[i+1]), 'pT%s'%(pTtag[i+1]), 100, 0, 500))
  phi.append(ROOT.TH1F('hphi%s'%(pTtag[i+1]), 'phi%s'%(pTtag[i+1]), 40, -3.2, 3.2))

hmsoft = ROOT.TH1F('hmSoft', 'm_soft [GeV]', 100, 0, 500)
hmhard = ROOT.TH1F('hmHard', 'm_hard [GeV]', 100, 0, 500)
hmall = ROOT.TH1F('hmAll', 'm_all [GeV]', 200, 0, 1000)
hmsofthardest = ROOT.TH1F('hmSoftHardest', 'm_softhardest [GeV]', 100, 0, 500)
hmhardsoftest = ROOT.TH1F('hmHardSoftest', 'm_hardsoftest [GeV]', 100, 0, 500)

while r.Next():
  vlist = []
  pTAll = []
  for j in range(4):
    vlist.append(ROOT.TLorentzVector())
    vlist[j].SetPx(px[j].Get()[0])
    vlist[j].SetPy(py[j].Get()[0])
    vlist[j].SetPz(pz[j].Get()[0])
    vlist[j].SetE(vlist[j].P())
    pTAll.append(vlist[j].Pt())
  pTsort = sorted(zip(pTAll,vlist))
  vlist_pT = [v for _, v in pTsort]
  for k in range(len(vlist_pT)):
    et[k].Fill(vlist_pT[k].Eta())
    phi[k].Fill(vlist_pT[k].Phi())
    pt[k].Fill(vlist_pT[k].Pt())
  vsoftpair = vlist_pT[0] + vlist_pT[1]
  hmsoft.Fill(vsoftpair.M())
  vhardpair = vlist_pT[2] + vlist_pT[3]
  hmhard.Fill(vhardpair.M())
  vall = vlist_pT[0] + vlist_pT[1] + vlist_pT[2] + vlist_pT[3]
  hmall.Fill(vall.M())
  vsofthardest = vlist_pT[1] + vlist_pT[3]
  hmsofthardest.Fill(vsofthardest.M())
  vhardsoftest = vlist_pT[2] + vlist_pT[0]
  hmhardsoftest.Fill(vhardsoftest.M())



c = ROOT.TCanvas('c', 'c', 800, 600)
for p in range(4):
  et[p].Draw()
  c.Update()
  c.Clear()
  phi[p].Draw()
  c.Update()
  c.Clear()
  pt[p].Draw()
  c.Update()
  c.Clear()
hmsoft.Draw()
c.Update()
c.Clear()
hmhard.Draw()
c.Update()
c.Clear()
hmall.Draw()
c.Update()
c.Clear()

fout.Write()
f.Close()
fout.Close()
