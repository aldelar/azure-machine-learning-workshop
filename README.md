# azure-machine-learning-workshop

A workshop leveraging Azure Machine Learning and introducing its key concepts and mode of operations. A Product overview is available here: https://azure.microsoft.com/en-us/services/machine-learning/#product-overview

# SETUP

1) Login to your subscription

    URL: https://portal.azure.com/

2) For all Azure resources, consider using a prefix that is short and tied to your identity to alleviate the possibilities of name collisions for the azure resources which are URIs.

For instance, consider a 2 or 3 letters prefix withlike: first letter of (first name, middle name, last name).

We'll call this 'prx' as in 'prefix' in the following notes.
Note that your prefix should be all lowercase to respect some of the resources naming limitations in Azure.

** Replace 'prx' with your own personal prefix everywhere below **

3) Pick a region from the following regions based on your locations:
East US, East US 2, SOuth Central US, West US 2

Create all resources below in the same selection region of your choice. The name of the resource between quotes "(name of resource)" is a good term to use in the search box when creating a resource in the Azure portal.

4) Create a "Resource Group" unless your Azure administrator already created one for you, in that case skip to step #5, but read NOTE (*) below

        Name:       prx-azure-ml-workshop
        Location:   region selected in step #3
    
    Region will not be specified in all instructions below, always set to it to the region you selected in step #3. This is sometimes automatically set if you create a new resource from within your resource group (it will try to default to your resource group's region).

    (*) If you have been assigned a resource group already, use it, even if it's not setup in your region of choice (see #3). A resource group is purely virtual and its region has no impact on the resources it contains. In such case, just create the other resources and make sure you specify your region of choice when creating your Azure services.

Everything else left as default (moving forward, when not specified, use the default paramters unless specified in the instructions)

Make sure that all resources below are created within your Resource Group (there will always be an option to change/set the resource group a resource belongs to, make sure it matches yours)

5) Create an Azure "Machine Learning" Workspace

        Workspace Name:     prx-mlws
        Workspace Edition:  Enterprise

6) Get into your Machine Learning workspace instance (created at step #5) and click on 'Launch Now' in the information box in the ML workspace panel.

You can also directly go to https://ml.azure.com/ and select the workspace created in step #5

This will lauch the 'Azure Machine Learning Studio' (referred to as AMLS moving foward) from which all ML resources can be managed and all your ML workflows can be built and executed, deployed from.

7) In AMLS, click on 'Compute' under 'Manage' to create some compute resources:

    7.a) Under 'Compute Instances', click on '+' to create a new notebook VM

        Compute name:           prx-notebook-vm
        Virtual Machine Size:   Standard_D3_v2 or similar (4 vCPUs, 14GB RAM)

        This notebook vm will be used as an editing platform for ml development, it is automatically pre-integrated with the rest of Azure ML.

    7.b) Under 'Training clusters', click on '+' to create a CPU based training cluster

        Compute name:                   prx-training-cpu
        Virtual Machine Size:           Standard_D3_v2 or similar (4 vCPUs, 14GB RAM)
        Minimal number of nodes:        0
        Maximum number of nodes:        4
        Idle seconds before scale down: 1200 (20 minutes to avoid shutdown/restart times during workshop)

    7.c) Under 'Training clusters', click on '+' to create a GPU based training cluster

        Compute name:                       prx-training-gpu
        Virtual Machine Size (click 'GPU'): Standard_NC6       
        Minimal number of nodes:            0
        Maximum number of nodes:            4
        Idle seconds before scale down:     1200 (20 minutes to avoid shutdown/restart times during workshop)

    The two clusters above are 'off' by default (no charge) and are created on-demand when workloads are executed. They autoscale up and all the way down to 0 (complete shutdown) based on the amount of ML workloads thrown at them (multiple ML workloads can be sent to the same clusters). The idle time controls how quickly they may completely shut down.

    This enables you to create many different clusters with various configurations (CPU intensive vs Memory intensive vs GPU intensive) and pick the best training cluster for the workload w/o actually paying for anything unless it actually runs (charge is by the minute, from the time a cluster is up, the time it takes to get the cluster up is at no charge).

    7.d) Under 'Inference clusters', click on '+' to create an inference cluster

        Compute name:           prx-inference
        Virtual Machine size:   Standard_D3_v2 or similar (4 vCPUs, 14GB RAM)
        Cluster purpose:        Dev-test
        Number of nodes:        1

        Inference clusters host your ML models deployments. Each deployment (aka ML endpoint) leads to a web service API that will run on an inference cluster. Multiple ML deployed endpoints can co-exist on the same inference clusters, or you can dedicate clusters to specific APIs. The clusters are Kubernetes managed clusters (Azure Kubernetes Service).

        You can also 'attach' existing clusters that your Azure administrators may be managing for you.

    NOTE: 'Attached compute' can also be leverage to 'bring your own compute' like a DataBricks cluster or specially tuned VMs of your choice.

8) Click on 'Notebooks' under 'Author'

    Mouse over 'Samples', click on the '...' icon to get the dropdown and select 'Clone' to clone the sample notebooks into your own environment. Select the default target (your own folder already pre-creared) as target and clone the samples into it.


# AUTHORING OPTIONS

They are 3 Types of experiences to Author ML in Azure ML Studio: Automated ML, Designer, and Notebooks. We will go thru each of them to understand their modes of operations. They all leverage the same underlying Azure ML concepts of Datastores, Datasets, Experimennts, Runs, Compute, etc. but just represent 3 ways to develop Machine Learning models covering the full spectrum from No-Code to Code-Only.

# AUTHORING WITH AUTOMATED ML
A) Automated ML: trains and finds the best model based on your data without writing a single line of code

We will create an Automated ML experiment to automatically train and find the best model to predict loan approvals based on applicants demographics.

A.1) Click on Datasets in the left side menu, and then Create Dataset 'from web file'

        Web URL:    https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv
        Name:       bank-marketing-training

A.2) On the next screen, keep all defaults except:

        Column headers:     All files have same headers

Have a quick look at the data to note that features in the training data set and the 'y' column which we are going to try to predict.

A.3) On the next screen, keep all defaults which should have auto-discovered the data types

A.4) On the 'Confirm Details' screen, check the 'Profile this dataset after creation' and select your 'prx-training-cpu' compute

A.5) Click 'Create'

Now that we have a dataset, we can click on it, review its content, profile, or potentially update it which will version it.

A.6) Click on 'Automated ML' in the left menu panel and click on 'new Automated ML'

A.7) Select your 'bank-marketing-training' dataset anc click Next

        Experiment name:            bank-marketing-loan-prediction
        Target column:              y
        Select training cluster:    prx-training-cpu

A.8) On the 'Select task type' screen, select 'Classification' and keep deep learning preview unchecked

Click on 'View additional configuration settings' and observe the parameters available to tune your ML run. No need to change anything. Note the concurrency setting which lets you control how many models run in parallel (one per cluster node max).

Click on 'View featurization settings' to see the controls related to featurization. By default all it automatic, but you could force a specific feature type or imputation model for each feature if needed. Leave all defaults.

A.9) Click on 'Finish' which creates the experiment and starts the execution

A.10) You can monitor the run from the experiment stage. If your cluster is idle, it may take a few minutes for things to kick off. Auto ML also first needs to generate a container image to run the models. The execution will also execute a 'Data guardrails' which will let you know about potential issues in your data for proper training.

We will let this experiment run and get back to it once it's in progress or completed.

Please feel free to check in the first few minutes what's happening, you'll see:
- in the logs the progress of the images being built and misc deployment preparation
- the Data guardrails complete with the results
- the Models being run

You can also go to the 'Compute' section, click on the 'prx-training-cpu' and you'll see the cluster progressively size up to its maximum size as the models get queued up. It should quickly reach its maximum size of 4 nodes as the Auto ML experiment will run about 50 models with this dataset to find the best one for this loan prediction.

As soon as a model completes under this Auto ML experiment, click on it to see its results, including its 'Visualizations' which will help you understand its performance.

Once the AutoML experiment completes, you'll be able to see the best model (auto sorted by Accuracy), look at its Details with Visualizations and its Explanation (auto computed for the best model).

A.11) Click on 'Deploy best model', or go to 'Models' and select the model you wish to deploy if the best selected model is not the one you want to deploy to solve your use case.

        Name:           bank-marketing-loan-prediction
        Compute name:   prx-inference

Click on 'Advanced':

        CPU reserve capacity:       0.1
        Memory reserve capacity:    0.1

Click on 'Deploy' to deploy the model. This will automatically generate a containerized web service deployed in Kubernetes.

Click on 'Endpoints' to monitor the deployment of this endpoint. Once it is completely deployed, you'll be able to access the auto generated Swagger JSON and get access to the 'Consume' endpoint.

# AUTHORING WITH THE DESIGNER
B) Designer: enables you to build Azure ML pipelines in a full Drag and Drop environment. This can be used for data preparation to generate training data sets, or end to end to train models.

B.1) Click on 'Designer' in the left menu, and under 'New pipeline', click on the 'Sample 1: Regression - Automobile Price Prediction...' sample to load it up.

B.2) Under 'Settings' which should pop up, select your 'prx-training-cpu' as the Default compute target

Observe the building blocks of this ML pipeline, from source DataSet, to data manipulations, data split, trainig, scoring and evaluation of the model.

To discover the source data set, click on it, then 'Outputs' and then the graphic icon to get a preview of the data with its profiling.

B.3) 'Submit' the experiment and select 'Create new' to create a new experiment

        New experiment name:    automobile-price-prediction

Click submit to run the experiment pipeline.

You can monitor the progress of the experiment directly from the current screen, you'll see the time icons next to each step conver to green checkmarks as things get executed. Behind the scenes, you just create another ML experiment, which means it's building container images, and starting up the training compute if it was idling.

Therefore, you can also monitor this experiment from the 'Experiments' left side menu item.

B.4) Once the experiment is completed, we can create inference endpoints (APIs)

Go to 'Designer', load your pipeline from the 'drafts' and click on 'Create inference pipeline'.
You have two options here to create two types of endpoints, a real time (one item at a time) endpoint or a batch endoint (batch processing to integrate within an ETL process for instance).

Select 'Real-time inference pipeline'.

The Designer automatically creates a new inference pipeline from the Training pipeline we've been working from, and adds a 'Web Service Input' and a 'Web Service Output' step automatically. This basically transforms our pipeline into a Web Service API. CLick on 'Submit' and then:

    Experiment:             Create New
    New experiment name:    automobile-price-prediction-realtime

Click 'Submit' and stay on the screen. The pipeline will quickly run to generate the code that will drive this web service.

Once it has completed, click on 'Deploy':

    Real-time endpoint name:        automobile-price-rt-endpoint
    Compute target:                 prx-inference

Click on deploy.

After a few moments, you'll be able to see your endpoint under 'Endpoints' in the left menu pane. The Swagger URI will be automatically generated as well as the consumption REST API endpoint. It may take a few minutes for the container images to be fully generated and deployed.

B.5) Modifying a Designer pipeline does not require a complete rerun. You'll be able to click on the different steps and review their outputs (logs or graphical visualizations) as well as modify them. The pipeline will only need to rerun what's changed and the dependencies, not every step. Its execution context is preserved to speed up iterative work.

Reload your original Designer pipeline and try the following:
- Click on the 'Split Data' step, and modify the split parameter from 0.7 to 0.8. Click on 'Submit' and select the previous experiment to re-execute it. Stay in place to observe the run re-executing only the steps that depend on the change.
- You can monitor and review the output of each step as they complete, without leaving the designer.

# AUTHORING WITH NOTEBOOKS
C) Notebooks