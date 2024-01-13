# The rationale for `datascribe`

With the increase in implementing artificial intelligence (AI) and machine learning systems around the world, there has been a drive to implement guidelines for best practice to address ethical concerns.  For example, the European Union produced [*Ethics Guidelines for Trustworthy Artificial Interlligence*](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai) in 2019, which highlights that trustworthy AI should be lawful, ethical and robust.  Within this document, seven key requirements have been listed which should be met to achieve trustworthy AI.  Requirement 4 is **transparency**: "including traceability, explainability and communication" (European Commission, 2019).  In addition, requirement 2 (technical robustness and safety) highlights the importance of creating reliable and reproducible AI systems.  The documentation highlights that key stakeholders in the process need to be able to accuraterly describe what the systems they use do.

While explainable AI tends to focus on the transparency and explainability of a particular model, it is important to consider transparency in any preprocessing techniques performed to prepare a dataset as well.  Clear documentation for research design is crucial in increasing the value of a study as it enables the research to be compared with other existing studies and inform future research (Ioannidis et al., 2014).

`datascribe` has been designed as a toolkit to help address these key concerns with AI.  The current version of the package provides a basic level of assistance to a data scientist or other individual who has decided to implement a logistic regresson model for predicting a binary outcome.  The package helps to map out the process undertaken to preprocess, clean up, model and then analyse the findings, using both written and visual communication formats.  While it cannot provide a fully comprehensive summary, it can help encourage the user on basic elements to include when they produce reports.  The output of the toolkit is markdown or Microsoft Word document format, which tend to be available to open and edit in both Linux and Windows operating systems and Free and Open Source Software (FOSS) tools.  These formats can be edited or incorporated into a final report.

The ultimate vision is to develop this functionality to other AI models to enable users to track and evaluate their models with ease, and most importantly, document what they have conducted to allow others to replicate the model and scrutinise the results.



## References

EUROPEAN COMMISSION. 2019. Ethics Guidelines for Trustworthy AI [Online]. Available: https://ec.europa.eu/futurium/en/ai-alliance-consultation/guidelines/1.html [Accessed 31 December 2023].

IOANNIDIS, J. P. A., GREENLAND, S., HLATKY, M. A., KHOURY, M. J., MACLEOD, M. R., MOHER, D., SCHULZ, K. F. & TIBSHIRANI, R. 2014. Increasing value and reducing waste in research design, conduct, and analysis. The Lancet, 383, 166-175.
