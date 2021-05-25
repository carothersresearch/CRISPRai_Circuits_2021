# File with different models and parameters for each

small_model = '''
dCas9_DNA -> dCas9_DNA + dCas9_ON; ktC*dCas9_DNA

SoxS_DNA -> SoxS_DNA + SoxS_ON; ktS*SoxS_DNA

RFP_DNA -> RFP_DNA + RFP_ON; ktR0*RFP_DNA

scRNA_DNA -> scRNA_DNA + scRNA; ktg10*scRNA_DNA
scRNA -> ; kdeg*scRNA

gRNA_DNA -> gRNA_DNA + gRNA; ktg20*gRNA_DNA
gRNA -> ; kdeg*gRNA

dCas9_ON + SoxS_ON + scRNA -> CRISPRa; ka*dCas9_ON*SoxS_ON*scRNA
dCas9_ON + gRNA -> CRISPRi; ki*dCas9_ON*SoxS_ON*gRNA


RFP_DNA + CRISPRa -> A_RFP_DNA; caskon*RFP_DNA*CRISPRa
A_RFP_DNA -> A_RFP_DNA + RFP_ON; ktR1*A_RFP_DNA

gRNA_DNA + CRISPRa -> A_gRNA_DNA; caskon*gRNA_DNA*CRISPRa
A_gRNA_DNA -> A_gRNA_DNA + gRNA; ktg21*A_gRNA_DNA

RFP_DNA + CRISPRi -> I_RFP_DNA; caskon*RFP_DNA*CRISPRi
A_RFP_DNA + CRISPRi -> I_RFP_DNA; caskon*A_RFP_DNA*CRISPRi
I_RFP_DNA + CRISPRa -> I_RFP_DNA; caskon*I_RFP_DNA*CRISPRa

ktC = {0}; ktS = {1}; ktR0 = {2}; 

ktg10 = {3}; ktg20 = {4};

ka = {5}; ki = {6};

ktR1 = {7}; ktg21 = {8};

caskon = {9}; kdeg = {10};

dCas9_DNA = {14}; SoxS_DNA = {15}; RFP_DNA = {11}; scRNA_DNA = {12}; gRNA_DNA = {13}

'''
small_model_params = ['ktC','ktS','ktR0','ktg10','ktg20','ka','ki','ktR1','ktg21','caskon','kdeg','RFP','scRNA','gRNA', 'dCas9','SoxS']

large_model = '''
    dCas9_DNA -> dCas9_DNA + dCas9_OFF; ktx1*dCas9_DNA
    dCas9_OFF -> dCas9_ON; kmat1*dCas9_OFF
    
    SoxS_DNA -> SoxS_DNA + SoxS_OFF; ktx1*SoxS_DNA
    SoxS_OFF -> SoxS_ON; kmat2*SoxS_OFF
    
    RFP_DNA -> RFP_DNA + RFP_OFF; ktx01*RFP_DNA
    RFP_OFF -> RFP_ON; kmat3*RFP_OFF
    
    scRNA_DNA -> scRNA_DNA + scRNA; ktx2*scRNA_DNA
    scRNA -> ; kdeg*scRNA
    
    gRNA_DNA -> gRNA_DNA + gRNA; ktx02*gRNA_DNA
    gRNA -> ; kdeg*gRNA
    
    dCas9_ON + SoxS_ON + scRNA -> CRISPRa; ka*dCas9_ON*SoxS_ON*scRNA
    dCas9_ON + gRNA -> CRISPRi; ki*dCas9_ON*SoxS_ON*gRNA

    
    RFP_DNA + CRISPRa -> A_RFP_DNA; caskon*RFP_DNA*CRISPRa
    A_RFP_DNA -> A_RFP_DNA + RFP_OFF; kta1*A_RFP_DNA
    
    gRNA_DNA + CRISPRa -> A_gRNA_DNA; caskon*gRNA_DNA*CRISPRa
    A_gRNA_DNA -> A_gRNA_DNA + gRNA; kta2*A_gRNA_DNA
    
    RFP_DNA + CRISPRi -> I_RFP_DNA; caskon*RFP_DNA*CRISPRi
    A_RFP_DNA + CRISPRi -> I_RFP_DNA; caskon*A_RFP_DNA*CRISPRi
    I_RFP_DNA + CRISPRa -> I_RFP_DNA; caskon*I_RFP_DNA*CRISPRa
    
    dCas9_DNA = 1; SoxS_DNA = 2; RFP_DNA = {14}; scRNA_DNA = {12}; gRNA_DNA = {13}
    
    ktx1 = {0}; ktx01 = {1}; ktx02 = {15}; 
    
    kmat1 = {2}; kmat2 = {3}; kmat3 = {4};
    
    ktx2 = {5}; kdeg = {6};
    
    ka = {7}; ki = {8};
    
    caskon = {9};
    
    kta1 = {10}; kta2 = {11};
'''
large_model_params = ['ktx1','ktx01','kmat1','kmat2','kmat3','ktx2','kdeg','ka','ki','caskon','kta1','kta2','scRNA','gRNA','RFP','ktx02']
