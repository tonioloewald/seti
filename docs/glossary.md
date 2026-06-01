> The glossary entries here were produced by Gemini from a copy of the pre-registration (June 1, 2026) across a few sessions — including <https://gemini.google.com/share/51f8d5d3b748> — and folded in by the investigator. Full AI-collaboration transcripts are archived in [`transcripts/`](transcripts/).

# Project Glossary

## The Detection Channels

To understand what we are searching for, it helps to know how we actually look at these stars. We do not take "pictures" of white dwarfs; we measure their light. An anomaly is a discrepancy between the light we expect to see and the light we actually measure.

### Channel A: The Spectral Energy Distribution (SED)

**The concept:** A Spectral Energy Distribution (SED) is a graph that plots how much energy a star emits across different colors (wavelengths) of light. Because white dwarfs are dead stars with no internal fusion, they cool down predictably. Their SED is a simple, smooth curve that drops off steeply in the infrared.

**The signal:** We are looking for an "infrared excess" — a bulge in the infrared part of the spectrum. This happens when something orbiting the star absorbs the star's optical light, heats up, and re-radiates that energy as heat.

**The anomaly:**
- *What is natural:* A warm debris disk (the shredded remains of an asteroid) or a brown dwarf companion.
- *What is anomalous:* An infrared excess with a temperature or shape that does not match standard rocky dust or known companions. The highest-value anomaly here is **dynamic** — an infrared excess that dramatically fluctuates over a decade of observations, suggesting active work rather than a passive, settling dust cloud.

### Channel B: Transit Light-Curve Morphology

**The concept:** A light curve is a graph of a star's brightness over time. If an object passes between the telescope and the star (a transit), the star's brightness temporarily dips.

**The signal:** Because white dwarfs are roughly the size of Earth, an orbiting object can block a massive fraction of their light, creating deep, highly visible transits.

**The anomaly:**
- *What is natural:* A spherical, intact planet produces a symmetric, U-shaped dip. Disintegrating asteroids (like those seen in the system WD 1145+017) leave long, messy dust tails, creating jagged, asymmetric dips.
- *What is anomalous:* A transit shape that is deeply asymmetric, flat-bottomed, perfectly square, or utterly irregular in a way that *cannot* be modeled by natural physics (spheres, rings, or disintegrating dust tails).

### Channel C: The Accretion-State / Inner-Zone Cleanliness

**The concept:** White dwarfs have incredibly strong gravity. Any heavy elements (metals) in their atmosphere should rapidly sink below the surface. If we see metals in a white dwarf's spectrum (a "polluted" white dwarf), it means the star is *actively* eating rocky material right now.

**The signal:** We look at stars that are actively polluted. Usually, this pollution is fed by a visible debris disk sitting right next to the star.

**The anomaly:**
- *What is natural:* A polluted star surrounded by a dusty, messy feeding disk.
- *What is anomalous:* A star that is heavily polluted, yet its immediate inner zone is completely clean and empty. If we can rule out natural clearing mechanisms, a perpetually clean inner zone despite active accretion implies a maintained, non-natural departure from standard debris physics.

## 1. Measurement & Observational Techniques

* **Difference-Image / Photocentroid Analysis**
When a telescope with large pixels (like TESS) sees a star dim, the dip might actually be a completely different background star in the same pixel undergoing an eclipse. This technique subtracts consecutive images or precisely tracks the "center of light" (centroid) to confirm the dimming is physically localized to the target white dwarf.
[Read more about Centroiding in Astronomy](https://en.wikipedia.org/wiki/Centroid_(astronomy))
* **Injection-Recovery**
A method for determining a pipeline's sensitivity (completeness). You artificially inject fake signals (synthetic IR excesses or transit dips) into the real, messy observational data, and then run your detection algorithm to see how many it successfully flags.
[Read more about Injection Testing](https://en.wikipedia.org/wiki/Software_testing#Fault_injection)
* **Light-Curve Morphology**
A light curve is a graph of a star's brightness over time. "Morphology" refers to the specific shape of any dips (transits). While a spherical planet creates a predictable U-shaped dip, an irregular, asymmetric, or flat-bottomed shape could indicate dust, debris tails, or an artificial construct.
[Read more about Transit Light Curves](https://en.wikipedia.org/wiki/Transit_(astronomy)#Light_curve)
* **Spectral Energy Distribution (SED) & IR Excess**
An SED is a graph showing how much energy an object emits across different wavelengths of light. A bare white dwarf has a predictable SED that drops off smoothly in the infrared. An "IR excess" is a bulge in that curve, indicating that something around the star is absorbing starlight and re-radiating it as heat.
[Read more about Spectral Energy Distributions](https://en.wikipedia.org/wiki/Spectral_energy_distribution)
* **Malmquist Bias**
**The concept:** An inescapable selection effect in astronomy. If you look at the night sky, you will easily see dim stars that are close to Earth, and you will only see distant stars if they are exceptionally bright.
**Why it matters:** Because this project requires high-quality data to run its tests, it will naturally exclude distant white dwarfs that are too faint for our telescopes to measure accurately. This creates a Malmquist bias: the project's final conclusions apply strictly to the *local* stellar neighborhood, not a perfect cross-section of the entire galaxy.
[Read more about Malmquist Bias](https://en.wikipedia.org/wiki/Malmquist_bias)
* **RUWE (Renormalized Unit Weight Error)**
**The concept:** A quality-control metric from the Gaia space telescope. Gaia measures the exact position of a star over time. If a star moves in a perfectly straight line, its RUWE is near 1.0. If the star wobbles unexpectedly, its RUWE spikes.
**Why it matters:** High RUWE usually means a star is being gravitationally tugged by an unseen companion (like a brown dwarf). Standard astronomical surveys throw out high-RUWE stars as "bad data." This project explicitly *keeps* them, because an unexpected wobble or a shifted center-of-light could be a clue to an anomaly.
* **BLS / TLS (Box-fitting Least Squares & Transit Least Squares)**
**The concept:** The standard algorithms used by astronomers to comb through millions of light curves looking for the tiny, periodic dips of a transit.
**Why it matters:** BLS is mathematically optimized to find square-shaped dips (like a solid block passing in front of a star). TLS is optimized to find U-shaped dips (like a spherical planet). Channel B uses these to flag initial events before checking if their morphology is completely weird.
[Read more about Box Least Squares](https://docs.astropy.org/en/stable/timeseries/bls.html)

## 2. Astrophysical Environments & Physics

* **Galactic Cirrus & The "Cirrus Ceiling"**
**The concept:** Just as Earth has wispy cirrus clouds, our Milky Way galaxy is filled with faint, cold clouds of interstellar dust. Because this dust is cold, it glows faintly in the far-infrared.
**Why it matters:** When looking for a cold anomaly around a distant white dwarf, we have to look *through* this galactic dust. The "cirrus ceiling" is the threshold where the background interstellar dust is simply too bright or too clumpy to reliably spot a faint infrared excess from the white dwarf itself. It's the observational equivalent of trying to see a flashlight through dense fog.
[Read more about Infrared Cirrus](https://en.wikipedia.org/wiki/Infrared_cirrus)
* **Poynting–Robertson Drag**
**The concept:** A quirk of orbital physics caused by radiation pressure. When a star's light hits a small grain of dust orbiting it, the dust grain absorbs the light and re-emits it. Because the grain is moving, this creates a microscopic braking effect, causing the dust to slowly lose momentum and spiral inward to be consumed by the star.
**Why it matters:** This is a "natural clearing mechanism" for Channel C. If a star has no dust in its inner zone, it might just be because Poynting–Robertson drag has already vacuumed it up naturally.
[Read more about the Poynting–Robertson Effect](https://en.wikipedia.org/wiki/Poynting%E2%80%93Robertson_effect)
* **Sublimation Radius**
**The concept:** The absolute closest a solid object (like a comet or dust grain) can get to a star before the intense heat causes it to instantly vaporize (sublimate) from a solid into a gas.
**Why it matters:** This is another natural clearing mechanism for Channel C. You wouldn't expect to see solid dust inside this radius because physics dictates it would burn away.
* **Photosphere & Photospheric Baseline**
**The concept:** The "surface" of a star — the layer where it becomes transparent and light can escape into space.
**Why it matters:** To find an anomaly, you have to know exactly what the bare star looks like. The "photospheric baseline" is the mathematical model of the light emitted *only* by the star's surface. We subtract this baseline from our telescope measurements; whatever is left over is the "excess."
* **Wien Tail**
**The concept:** Every warm object emits a spectrum of light (a blackbody curve) that peaks at a certain wavelength and trails off on either side. The "Wien tail" is the short-wavelength (higher-energy) slope of this curve.
**Why it matters:** If an anomaly is extremely cold (e.g., 30 Kelvin), almost all of its light is emitted in the far-infrared. The WISE telescope's longest wavelength band (W4) can only just barely catch the very edge — the Wien tail — of that cold light, making cold anomalies notoriously difficult to detect with current data.
[Read more about Wien's Displacement Law](https://en.wikipedia.org/wiki/Wien%27s_displacement_law)

## 3. Statistical & Analytical Methods

* **Bonferroni Correction & The Trial Factor**
When you run 100,000 tests, a "1-in-10,000" statistical fluke is guaranteed to happen roughly 10 times. To avoid drowning in false positives, you apply a "trial factor" penalty. The Bonferroni correction is the most conservative version of this: if your desired false positive rate is $\alpha$, you require a significance of $\alpha / N$ (where $N$ is the number of tests).
[Read more about the Bonferroni Correction](https://en.wikipedia.org/wiki/Bonferroni_correction)
* **Censored Likelihood**
A statistical technique for handling "non-detections." If a telescope looks for a signal but doesn't see one, that isn't a "zero"—it means the signal is *somewhere below* the telescope's sensitivity limit. Censored likelihood models these upper bounds mathematically instead of throwing the data away.
[Read more about Censored Regression](https://en.wikipedia.org/wiki/Censored_regression_model)
* **Empirical Null & Local FDR**
Standard statistics often assumes noise follows a perfect, theoretical bell curve (the "theoretical null"). In real-world data with instrumental quirks, the actual noise distribution is often wider. The "empirical null" builds the baseline normal distribution out of the bulk of the actual data itself, ensuring anomalies are judged against reality, not theory.
[Read more about Empirical Null Distribution](https://en.wikipedia.org/wiki/False_discovery_rate#Local_false_discovery_rate)
* **False Discovery Rate (FDR) / Benjamini–Hochberg Procedure**
A way to manage false positives in large datasets. Instead of strictly trying to prevent *any* false positives (which kills your ability to find faint signals), FDR controls the *proportion* of false positives among the subset of items you flag as interesting.
[Read more about False Discovery Rate](https://en.wikipedia.org/wiki/False_discovery_rate)
* **Genomic-Control Inflation Factor ($\lambda$)**
A single diagnostic number borrowed from genetics. It measures how much the real, empirical noise in your dataset exceeds the theoretical ideal. If $\lambda \approx 1$, the theoretical math works perfectly. If $\lambda > 1$, your noise is inflated, and you must use the empirical null.
[Read more about Genomic Control](https://en.wikipedia.org/wiki/Genomic_control)
* **Look-Elsewhere Effect / Gross-Vitells Method**
A physics term for the statistical penalty you pay when searching a large parameter space (like scanning for an anomaly across a wide range of temperatures). Gross-Vitells is a specific, computationally efficient mathematical method for calculating this penalty when tests are correlated, heavily used in particle physics (e.g., finding the Higgs Boson).
[Read more about the Look-Elsewhere Effect](https://en.wikipedia.org/wiki/Look-elsewhere_effect)
* **Poisson Bound (Zero-Detection Limit)**
A mathematical way to state an upper limit when you find absolutely nothing. If you observe zero anomalies, the Poisson distribution dictates that you can be 95% confident the true average rate is less than 3.0 divided by your sample size (adjusted for your pipeline's sensitivity).
[Read more about Poisson Confidence Intervals](https://en.wikipedia.org/wiki/Poisson_distribution#Confidence_interval)
* **Quantile-Quantile (Q-Q) Plot**
A visual diagnostic tool. It plots your actual observed data distribution against the expected theoretical distribution. If your data is well-behaved, it tracks a straight diagonal line. True anomalies will visually peel away from the line at the extreme upper right.
[Read more about Q-Q Plots](https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot)

---

## 4. Cited Literature & Papers

### The "Assumed Mechanism" SETI Baseline

*These papers represent the traditional technosignature approaches this project explicitly departs from by removing assumptions about what a civilization would build.*

* **Dyson (1960)** · *Search for Artificial Stellar Sources of Infrared Radiation*
**Thrust:** The foundational paper proposing that advanced civilizations might enclose their host stars to capture energy, radiating the waste heat in the infrared.
[Link to Paper (Science)](https://doi.org/10.1126/science.131.3414.1667)
* **Landauer (1961)** · *Irreversibility and Heat Generation in the Computing Process*
**Thrust:** Establishes the physical lower limit of energy consumption for computation. Frequently used in SETI to argue that advanced tech would trend extremely cold for maximum thermodynamic efficiency.
[Link to Paper (IBM)](https://doi.org/10.1147/rd.53.0183)
* **Kardashev (1964)** · *Transmission of Information by Extraterrestrial Civilizations*
**Thrust:** Proposes the famous scale categorizing civilizations by their gross energy consumption (Planetary, Stellar, Galactic).
[Link to Paper (ADS)](https://ui.adsabs.harvard.edu/abs/1964SvA.....8..217K/abstract)
* **Sandberg, Armstrong & Ćirković (2017)** · *That is not dead which can eternal lie: the aestivation hypothesis...*
**Thrust:** Proposes that advanced civilizations might purposefully power down and "sleep" until the universe cools down to maximize computational efficiency, making them incredibly cold and hard to see today.
[Link to Paper (arXiv)](https://arxiv.org/abs/1705.03394)
* **Zuckerman (2022)** · *Infrared and optical detectability of Dyson spheres at white dwarf stars*
**Thrust:** A targeted search for Dyson spheres around white dwarfs, but explicitly limited to *warm* constructs (300–1000 K), which happens to be the exact temperature where natural debris disks also live.
[Link to Paper (arXiv)](https://arxiv.org/abs/2204.09627)
* **Suazo et al. (2024)** · *Project Hephaistos – II. Dyson sphere candidates from Gaia DR3, 2MASS, and WISE*
**Thrust:** A large-scale search for partial Dyson spheres around main-sequence stars, looking for warm excess signatures.
[Link to Paper (arXiv)](https://arxiv.org/abs/2405.02927)
* **Wright et al. (2014, 2016) / Griffith et al. (2015)** · *The Ĝ Infrared Search (G-HAT)*
**Thrust:** A search for galaxy-spanning (Kardashev Type III) civilizations by looking for massive amounts of mid-infrared waste heat.
[Link to Paper I (arXiv)](https://arxiv.org/abs/1408.1133)

### Anomalous Transits & Statistical Philosophy

*Literature establishing the methodology of looking for structural anomalies in light curves and properly calibrating large surveys.*

* **Arnold (2005)** · *Transit Lightcurve Signatures of Artificial Objects*
**Thrust:** Demonstrates mathematically that non-spherical objects (like artificial megastructures or louvers) produce uniquely identifiable, asymmetric light curve signatures distinct from natural planets.
[Link to Paper (arXiv)](https://arxiv.org/abs/astro-ph/0503580)
* **Boyajian et al. (2016)** · *Planet Hunters IX. KIC 8462852 — Where's the Flux?*
**Thrust:** The famous "Tabby's Star" paper. An excellent case study in detecting a wildly anomalous, highly structured, aperiodic light curve and methodically trying (and failing) to explain it with standard natural phenomena.
[Link to Paper (arXiv)](https://arxiv.org/abs/1509.03622)
* **Sandberg, Drexler & Ord (2018)** · *Dissolving the Fermi Paradox*
**Thrust:** Argues that if you properly account for the massive uncertainty in the Drake Equation (using probability distributions instead of point estimates), the most likely mathematical outcome is that we are effectively alone, thus there is no "paradox."
[Link to Paper (arXiv)](https://arxiv.org/abs/1806.02404)
* **Jenkins, Caldwell & Borucki (2002)** · *Some Tests to Establish Confidence in Planets Discovered by Transit Photometry*
**Thrust:** The paper establishing the $7.1\sigma$ detection threshold for the Kepler mission, calculated specifically so that random statistical noise wouldn't trigger more than 1 false alarm across 150,000 target stars.
[Link to Paper (ADS)](https://ui.adsabs.harvard.edu/abs/2002ApJ...564..495J/abstract)

### White Dwarf Astrophysics

*The natural baseline against which this project searches for anomalies.*

* **Farihi (2016)** · *Circumstellar debris and pollution at white dwarf stars*
**Thrust:** The definitive modern review of how natural debris disks form, evolve, and pollute the atmospheres of white dwarfs.
[Link to Paper (arXiv)](https://arxiv.org/abs/1604.03092)
* **Gentile Fusillo et al. (2021)** · *A catalogue of white dwarfs in Gaia EDR3*
**Thrust:** The primary target list for this project. Uses Gaia astrometry and machine learning to compile a highly reliable catalog of over 350,000 high-confidence white dwarfs.
[Link to Paper (arXiv)](https://arxiv.org/abs/2106.07669)
* **Vanderburg et al. (2020)** · *A giant planet candidate transiting a white dwarf*
**Thrust:** The discovery of WD 1856+534 b, proving that large, intact planetary bodies can survive the red giant phase and establish tight, transiting orbits around white dwarfs.
[Link to Paper (arXiv)](https://arxiv.org/abs/2009.07282)
* **Agol (2011)** · *Transit Surveys for Earths in the Habitable Zones of White Dwarfs*
**Thrust:** Calculates that because white dwarfs are so small, planets orbiting in their (very tight) habitable zones would create deep, easily detectable transits with periods of mere hours.
[Link to Paper (arXiv)](https://arxiv.org/abs/1103.2791)

---

## Possible Outcomes & Interpretation

This project deliberately uncouples the *search for anomalies* from the *claim of finding intelligence*. The discipline of the search is recognizing exactly what the data does and does not allow us to say.

### Outcome 1: The Null Result (Expected)

**What it looks like:** Every candidate flagged by the pipeline is successfully explained away. The anomalous light curves turn out to be background eclipsing binaries or telescope artifacts. The infrared excesses turn out to be natural dust disks, brown dwarfs, or background interstellar cirrus clouds. The final catalog of unexplained anomalies is zero.

**What it means:** This is a successful, quantifiable scientific result. It allows us to mathematically set an upper limit on prevalence: *"Fewer than X% of white dwarfs in the local stellar neighborhood host unexplained, macro-scale anomalies."* It tightens our understanding of what exists in the universe.

**What it DOES NOT mean:**
- It does not mean "we are alone."
- It does not mean advanced civilizations don't exist. It simply means that if they do exist, they do not build massive, thermodynamic-altering megastructures around white dwarfs that happen to be visible in our current legacy infrared and transit data.

### Outcome 2: A Surviving Residual (The "Anomaly")

**What it looks like:** One or more white dwarfs exhibit a signal (e.g., a massive, fluctuating cold infrared excess, or a highly structured transit shape) that survives the entire gauntlet of natural explanations. It cannot be explained by dust, companions, telescope errors, or background noise.

**What it means:** We have discovered **previously unknown, unmodeled astrophysics**. It means our current understanding of how stellar remnants, debris disks, or low-mass companions behave is incomplete. We publish the anomaly catalog and hand it to the astrophysical community so that larger telescopes (like JWST) can point at these specific stars to figure out what new physical mechanism is at play.

**What it DOES NOT mean:**
- It absolutely does **not** mean "we found an alien megastructure."
- To declare a surviving anomaly to be a "technosignature" is a failure of scientific rigor. "Unexplained by current models" simply means the models have a gap. The highest-probability explanation for any surviving anomaly is *always* new natural physics, and the project strictly enforces this boundary.
