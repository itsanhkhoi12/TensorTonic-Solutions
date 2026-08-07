# TensorTonic Solutions

Welcome to my TensorTonic solutions repository!

Here you'll find my solutions to various machine learning and deep learning problems from [TensorTonic](https://tensortonic.com).

## What is TensorTonic?

TensorTonic is a platform where you can implement core algorithms of Machine Learning from scratch.

This repository contains my personal solutions to these problems, automatically synchronized from the platform.

<!-- tensortonic:start -->
# Anh Khoi's TensorTonic Solutions

Verified machine learning implementations completed on [TensorTonic](https://www.tensortonic.com).

<p align="center">
  <img src="https://www.tensortonic.com/api/badge/akoisukho.svg" alt="TensorTonic Verified Solutions" width="100%" />
</p>

| Problem | Description | Link |
|---|---|---|
| AdaGrad Optimizer | Implement a vectorized AdaGrad update in NumPy with accumulated squared gradients and adaptive per-parameter learning rates. | https://www.tensortonic.com/problems/adagrad-optimizer |
| Implement Adam Optimizer Step | Implement one vectorized Adam optimizer step in NumPy with first and second moments, bias correction, and elementwise parameter updates. | https://www.tensortonic.com/problems/adam-optimizer |
| Implement AdamW (Decoupled Weight Decay) | Implement one AdamW optimizer step in NumPy with first and second moments plus decoupled weight decay. | https://www.tensortonic.com/problems/adamw-optimizer |
| Bag-of-Words Vector | Build a NumPy bag-of-words count vector from an ordered vocabulary while ignoring out-of-vocabulary tokens. | https://www.tensortonic.com/problems/bag-of-words |
| Bernoulli Probability Mass Function & Moments | Compute the Bernoulli probability mass function, expected value, and variance for a valid success probability. | https://www.tensortonic.com/problems/bernoulli-pmf |
| Binning | Assign numeric values to ordered bins using supplied boundaries while handling values at interval edges. | https://www.tensortonic.com/problems/binning |
| BLEU Score | Calculate a BLEU translation score from candidate and reference tokens using clipped n-gram precision and brevity penalty. | https://www.tensortonic.com/problems/bleu-score |
| Catalog Coverage | Measure recommendation catalog coverage as the fraction of available items appearing across user recommendation lists. | https://www.tensortonic.com/problems/catalog-coverage |
| Cohen's Kappa | Calculate Cohen's kappa from two label sequences by comparing observed agreement with chance agreement. | https://www.tensortonic.com/problems/cohens-kappa |
| Color to Grayscale | Convert an RGB image to grayscale using weighted color channels while preserving its spatial dimensions. | https://www.tensortonic.com/problems/color-to-grayscale |
| Cosine Annealing LR Scheduler | Compute a cosine-annealed learning rate between configured maximum and minimum values across training steps. | https://www.tensortonic.com/problems/cosine-annealing-lr |
| Implement Cosine Similarity | Compute cosine similarity between NumPy vectors with dot products, Euclidean norms, and zero-vector handling. | https://www.tensortonic.com/problems/cosine-similarity |
| Cyclic Encoding | Encode periodic numeric features as sine and cosine coordinates using a specified cycle length. | https://www.tensortonic.com/problems/cyclic-encoding |
| Data Drift Detection | Detect feature drift by computing total variation distance between reference and production histograms. | https://www.tensortonic.com/problems/data-drift-detection |
| Implement Dot Product | Implement the dot product of equal-length numeric vectors by summing element-wise products without library shortcuts. | https://www.tensortonic.com/problems/dot-product |
| ELU Activation | Apply the ELU activation element-wise, retaining positive inputs and exponentially transforming negative values. | https://www.tensortonic.com/problems/elu-activation |
| ETL Deduplication | Deduplicate ETL records by configured key fields while applying the required policy for repeated entries. | https://www.tensortonic.com/problems/etl-deduplication |
| ETL Dependency Orchestration | Resolve ETL job dependencies into a valid execution order while detecting missing or cyclic dependencies. | https://www.tensortonic.com/problems/etl-dependency-orchestration |
| ETL Schema Validation | Validate ETL records against required field names and data types, reporting rows that violate the schema. | https://www.tensortonic.com/problems/etl-schema-validation |
| Implement Euclidean Distance | Compute Euclidean distance between equal-length NumPy vectors as the square root of summed squared differences. | https://www.tensortonic.com/problems/euclidean-distance |
| Expected Value (Discrete Distribution) | Compute the expected value of a discrete distribution from matched outcomes and normalized probabilities. | https://www.tensortonic.com/problems/expected-value-discrete |
| Exponential Moving Average | Calculate an exponential moving average across a time series using the configured smoothing factor. | https://www.tensortonic.com/problems/exponential-moving-average |
| Feature Store Lookup | Combine stored offline and request-time features in input order, using defaults for unknown user IDs. | https://www.tensortonic.com/problems/feature-store-lookup |
| Frequency Encoding | Replace categorical values with their observed frequencies while preserving the original sequence order. | https://www.tensortonic.com/problems/frequency-encoding |
| Implement GELU Activation (Gaussian Error Linear Unit) | Implement the Gaussian Error Linear Unit activation element-wise using the required GELU approximation. | https://www.tensortonic.com/problems/gelu |
| Geometric Probability Mass Function & Mean | Compute the geometric distribution probability mass and mean from a valid success probability. | https://www.tensortonic.com/problems/geometric-pmf-mean |
| Gradient Clipping (Global Norm) | Clip a NumPy gradient array by its global L2 norm while preserving direction when scaling is required. | https://www.tensortonic.com/problems/gradient-clipping |
| Implement Gradient Descent for a 1D Quadratic | Optimize a one-dimensional quadratic with iterative gradient descent and return the parameter trajectory. | https://www.tensortonic.com/problems/gradient-descent-quadratic |
| He Initialization | Scale raw weights into the He uniform range using a bound derived from the layer fan-in. | https://www.tensortonic.com/problems/he-initialization |
| Hit Rate at K | Calculate recommendation hit rate at K by checking whether each user's relevant items appear in top-ranked results. | https://www.tensortonic.com/problems/hit-rate-at-k |
| Implement Huber Loss | Compute Huber loss with quadratic errors near zero and linear penalties beyond a configurable threshold. | https://www.tensortonic.com/problems/huber-loss |
| Image Histogram | Count grayscale image pixels into intensity bins and return the histogram in ascending intensity order. | https://www.tensortonic.com/problems/image-histogram |
| Item-Based CF Prediction | Predict a user-item rating with item-based collaborative filtering from rated neighbors and item similarities. | https://www.tensortonic.com/problems/item-cf-predict |
| Jaccard Similarity | Compute Jaccard similarity between two collections as intersection size divided by union size. | https://www.tensortonic.com/problems/jaccard-similarity |
| Implement Leaky ReLU (with α) | Apply Leaky ReLU element-wise with a configurable negative slope while retaining positive inputs. | https://www.tensortonic.com/problems/leaky-relu |
| Linear Layer Forward | Implement a dense linear layer forward pass by multiplying inputs by weights and adding a bias vector. | https://www.tensortonic.com/problems/linear-layer-forward |
| Learning Rate Scheduler (Linear Decay) | Compute a linearly decaying learning rate across training steps between configured start and end values. | https://www.tensortonic.com/problems/linear-lr-scheduler |
| Linear Regression Closed Form | Fit linear regression with the closed-form normal equation and return coefficients for the supplied design matrix. | https://www.tensortonic.com/problems/linear-regression-closed-form |
| Log Loss (Per-Sample) | Compute binary log loss for each prediction with clipped probabilities to prevent undefined logarithms. | https://www.tensortonic.com/problems/log-loss-per-sample |
| Log Transform | Apply a numerically safe logarithmic transform to numeric features using the required offset or base. | https://www.tensortonic.com/problems/log-transform |
| Logistic Regression Training Loop | Train binary logistic regression in NumPy using sigmoid probabilities, gradient descent, and learned weight and bias parameters. | https://www.tensortonic.com/problems/logistic-regression-training |
| Make Diagonal Matrix | Construct a square diagonal matrix from a one-dimensional vector while setting every off-diagonal entry to zero. | https://www.tensortonic.com/problems/make-diagonal |
| Implement Manhattan Distance | Compute Manhattan distance between equal-length vectors by summing absolute coordinate differences. | https://www.tensortonic.com/problems/manhattan-distance |
| Matrix Factorization SGD Step | Perform one matrix-factorization SGD update for a rated user-item pair with latent factors and regularization. | https://www.tensortonic.com/problems/matrix-factorization-sgd-step |
| Implement Matrix Normalization | Normalize a NumPy matrix using the specified axis and norm while safely handling zero-magnitude slices. | https://www.tensortonic.com/problems/matrix-normalization |
| Matrix Trace | Compute the trace of a square matrix by summing its main diagonal entries without changing the input. | https://www.tensortonic.com/problems/matrix-trace |
| Matrix Transpose | Implement matrix transpose in NumPy without built-in transpose helpers, preserving rectangular shapes and the original input. | https://www.tensortonic.com/problems/matrix-transpose |
| Mean, Median, Mode | Calculate the mean, median, and deterministic mode of a numeric collection, including tied frequencies. | https://www.tensortonic.com/problems/mean-median-mode |
| Mean Squared Error (MSE) | Compute mean squared error between predictions and targets by averaging their squared element-wise differences. | https://www.tensortonic.com/problems/mean-squared-error |
| Implement Micro-F1 | Compute multiclass micro-F1 by aggregating true positives, false positives, and false negatives across labels. | https://www.tensortonic.com/problems/metrics-f1-micro |
| Min-Max Scaling | Scale numeric values to a requested range using observed minimum and maximum values with constant-input handling. | https://www.tensortonic.com/problems/min-max-scaling |
| Implement Min-Max Normalization | Normalize each NumPy feature to the zero-to-one range with explicit handling for constant columns. | https://www.tensortonic.com/problems/minmax-normalization |
| Model Versioning | Select a production model by highest accuracy, then lower latency, then the most recent timestamp. | https://www.tensortonic.com/problems/model-versioning-basics |
| Monitoring Metrics Selection | Compute the required monitoring metrics for classification, regression, or ranking prediction results. | https://www.tensortonic.com/problems/monitoring-metrics-selection |
| NDCG (Normalized Discounted Cumulative Gain) | Calculate normalized discounted cumulative gain at K from ranked relevance scores and their ideal ordering. | https://www.tensortonic.com/problems/ndcg |
| Implement Nesterov Momentum (NAG) | Implement a Nesterov accelerated-gradient update using lookahead momentum and the current gradient. | https://www.tensortonic.com/problems/nesterov-momentum |
| One-Hot Encoding (Multi-class) | Convert multiclass integer labels into a NumPy one-hot matrix with one active column per sample. | https://www.tensortonic.com/problems/one-hot-encoding |
| Ordinal Encoding | Map ordered categorical values to integer ranks using a supplied category ordering and preserve input order. | https://www.tensortonic.com/problems/ordinal-encoding |
| Pad Sequences | Pad or truncate variable-length token ID sequences in NumPy with configurable maximum length and padding values. | https://www.tensortonic.com/problems/pad-sequences |
| Percent Change | Compute period-over-period percentage changes in a numeric time series with defined initial-value handling. | https://www.tensortonic.com/problems/percent-change |
| Perplexity Computation | Compute language-model perplexity from token probability distributions and the observed token indices. | https://www.tensortonic.com/problems/perplexity-computation |
| Polynomial Features | Expand numeric inputs into polynomial features through a specified degree using deterministic column ordering. | https://www.tensortonic.com/problems/polynomial-features |
| Popularity Ranking | Rank items by interaction popularity with deterministic ordering for equal-frequency items. | https://www.tensortonic.com/problems/popularity-ranking |
| Precision and Recall at K | Compute recommendation precision and recall at K by comparing ranked predictions with relevant items. | https://www.tensortonic.com/problems/precision-recall-at-k |
| Tabular Q-Learning (Single Update) | Perform one tabular Q-learning update from reward, discount, learning rate, and the best next-state value. | https://www.tensortonic.com/problems/q-learning-update |
| Implement R² Score (Coefficient of Determination) | Compute the coefficient of determination from targets and predictions with explicit constant-target handling. | https://www.tensortonic.com/problems/r2-score |
| Rank Transform | Replace numeric values with their ranks while applying the specified policy to tied observations. | https://www.tensortonic.com/problems/rank-transform |
| Implement ReLU Activation | Apply the ReLU activation element-wise by replacing negative values with zero and preserving nonnegative inputs. | https://www.tensortonic.com/problems/relu-activation |
| Remove Stopwords | Remove tokens found in a supplied stopword collection while preserving the order of remaining words. | https://www.tensortonic.com/problems/remove-stopwords |
| Retraining Trigger Design | Evaluate production monitoring signals and decide whether they satisfy the configured model-retraining policy. | https://www.tensortonic.com/problems/retraining-trigger-design |
| RMSProp Optimizer (Single Update Step) | Implement one RMSProp update in NumPy using an exponential squared-gradient average and adaptive scaling. | https://www.tensortonic.com/problems/rmsprop-optimizer |
| RNN Step Forward (Tanh Cell) | Implement one vanilla RNN timestep with affine input and recurrent transforms followed by tanh activation. | https://www.tensortonic.com/problems/rnn-step-forward |
| Robust Scaling | Scale numeric features using their median and interquartile range with constant-spread handling. | https://www.tensortonic.com/problems/robust-scaling |
| Sample Variance & Standard Deviation | Compute sample variance and standard deviation with Bessel's correction from a numeric collection. | https://www.tensortonic.com/problems/sample-var-std |
| Seasonal Average | Estimate seasonal averages by grouping time-series observations at the same position in each period. | https://www.tensortonic.com/problems/seasonal-average |
| SELU Activation | Apply SELU activation element-wise with scaled positive values and exponential negative values. | https://www.tensortonic.com/problems/selu-activation |
| Shadow Deployment Evaluation | Compare shadow and production model outcomes using the evaluation criteria defined by the problem. | https://www.tensortonic.com/problems/shadow-deployment-evaluation |
| Implement Sigmoid in NumPy | Implement a vectorized sigmoid activation in NumPy for scalars, lists, vectors, and matrices, including large positive and negative inputs. | https://www.tensortonic.com/problems/sigmoid-numpy |
| Implement Softmax Function | Implement numerically stable softmax by shifting logits before exponentiation and normalizing probabilities. | https://www.tensortonic.com/problems/softmax-function |
| Implement Swish Activation | Apply the Swish activation element-wise by multiplying each input by its sigmoid value. | https://www.tensortonic.com/problems/swish-activation |
| One-Sample t-Test | Compute a one-sample t-statistic in NumPy using the sample mean, Bessel-corrected deviation, and hypothesized mean. | https://www.tensortonic.com/problems/t-test-one-sample |
| Implement Tanh Activation | Implement the hyperbolic tangent activation element-wise with outputs bounded between minus one and one. | https://www.tensortonic.com/problems/tanh-activation |
| One-Step TD Value Update | Perform one temporal-difference value update from reward, discount, next-state value, and learning rate. | https://www.tensortonic.com/problems/td-value-update |
| Text Chunking | Split text into ordered chunks under the requested size and overlap rules without dropping content. | https://www.tensortonic.com/problems/text-chunking |
| Top-K Recommendations | Return each user's highest-scoring unseen items with deterministic ranking and a configurable result limit. | https://www.tensortonic.com/problems/top-k-recommendations |
| Detect Train-Serving Skew | Detect train-serving skew by comparing offline and online feature values under configured tolerances. | https://www.tensortonic.com/problems/train-serving-skew |
| User-Based CF Prediction | Predict a user-item rating from similar users' ratings with neighborhood weighting and mean adjustment. | https://www.tensortonic.com/problems/user-based-cf-prediction |
| Compute 3D Vector Norm | Compute the Euclidean norm of a 3D vector from the square root of summed squared coordinates. | https://www.tensortonic.com/problems/vector-norm-3d |
| Warmup + Linear Decay LR Schedule | Compute a learning-rate schedule with linear warmup followed by linear decay across training steps. | https://www.tensortonic.com/problems/warmup-decay-lr |
| Word Count Dictionary | Count token occurrences in text and return a dictionary mapping each distinct word to its frequency. | https://www.tensortonic.com/problems/word-count-dict |
| Xavier Initialization | Scale raw weights into the Xavier uniform range using a bound derived from fan-in and fan-out. | https://www.tensortonic.com/problems/xavier-initialization |
| Implement z-Score Standardization | Standardize NumPy features to zero mean and unit variance with explicit handling for constant columns. | https://www.tensortonic.com/problems/zscore-standardization |
| Frequent-Word Subsampling | Implement Word2Vec frequent-word subsampling by computing token retention probabilities from corpus frequencies. | https://www.tensortonic.com/research/word2vec/word2vec-subsampling |

View my verified ML profile: [TensorTonic profile](https://www.tensortonic.com/profile/akoisukho)
<!-- tensortonic:end -->
