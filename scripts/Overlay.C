#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <iostream>


void overlayHistograms(const char* fileName, const char* histName1, const char* histName2, int fitLineColor)
{
    // Open the ROOT file
    TFile* file = new TFile(fileName);
    if (!file || file->IsZombie()) {
        std::cerr << "Error opening file: " << fileName << std::endl;
        return;
    }

    // Retrieve the histograms
    TH1* hist1 = dynamic_cast<TH1*>(file->Get(histName1));
    TH1* hist2 = dynamic_cast<TH1*>(file->Get(histName2));

    if (!hist1 || !hist2) {
        std::cerr << "Error retrieving histograms: " << histName1 << ", " << histName2 << std::endl;
        file->Close();
        return;
    }

    // Create a new canvas
    TCanvas* canvas = new TCanvas("canvas", "Overlay Histograms", 800, 600);

    // Overlay the histograms
    hist1->SetLineColor(kRed);
    hist2->SetLineColor(kBlue);

    hist1->Draw();
    hist2->Draw("SAME");

    // Get the fit functions for the histograms
    TF1* fitFunc1 = hist1->GetFunction("pmt");
    TF1* fitFunc2 = hist2->GetFunction("pmt");

    // Set the line color for the fit functions
    fitFunc1->SetLineColor(kRed);
    fitFunc2->SetLineColor(fitLineColor);

    // Add a legend
    TLegend* legend = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend->AddEntry(hist1, histName1, "l");
    legend->AddEntry(hist2, histName2, "l");
    legend->Draw();

    // Save the canvas as an image
    std::string outputFileName = std::string("combined_") + histName1 + "_" + histName2 + ".root";
    canvas->SaveAs(outputFileName.c_str());

    // Cleanup
    file->Close();
    delete file;
    delete canvas;
}

int main()
{
    const char* fileName = "Integrated.root";
    const char* histName1 = "h220720_1";
    const char* histName2 = "h220721_2";
    int fitLineColor = kBlue;  // Specify the desired line color for the fit line of hist2, e.g., kGreen

    overlayHistograms(fileName, histName1, histName2, fitLineColor);

    return 0;
}
