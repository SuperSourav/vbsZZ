import ROOT


def plot(f1, f2, hist):
  ROOT.gROOT.SetBatch(1)
  h1 = f1.Get(hist)
  h2 = f2.Get(hist)
  h1.Scale(1./h1.Integral()) #normalize
  h2.Scale(1./h2.Integral())
  c = ROOT.TCanvas('c', 'c', 800, 600)
  h1.SetMaximum(1.04*max(h1.GetMaximum(),h2.GetMaximum()))
  h1.SetLineColor(1)
  h2.SetLineColor(2)
  leg = ROOT.TLegend( 0.65, 0.75, 0.88, 0.90 )
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.AddEntry(h1, "events1", "L") #hardcoded legends!
  leg.AddEntry(h2, "events2", "L")
  h1.SetStats(0) #stat box switched off
  h2.SetStats(0)
  h1.Draw()
  h2.Draw('same')
  leg.Draw()
  c.Update()
  c.Print(hist+".eps")
  c.Clear()


def main():
  f1 = ROOT.TFile("/afs/cern.ch/user/a/akotwal/work/analysis/vbsZZ/events1MergedMomenta.root")
  f2 = ROOT.TFile("/afs/cern.ch/user/a/akotwal/work/analysis/vbsZZ/events2MergedMomenta.root")

 # get the list of TH1F names
  f1.cd()
  histnames = [h.ReadObj().GetName() for h in f1.GetListOfKeys()]
 # overlay
  for h in histnames:
    plot(f1,f2,h) 


if __name__ == '__main__':
  main()
