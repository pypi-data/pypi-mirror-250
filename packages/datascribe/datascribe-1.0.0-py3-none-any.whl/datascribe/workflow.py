'''
Workflow class to create a graphviz workflow from data preprocessing
and analysis.

'''

import graphviz
import os


class Workflow:
    '''
    Workflow class stores the attributes and methods linked to
    producing a graphviz workflow image output.
    '''
    def __init__(self, scribe):
        '''
        Initiator method for Workflow.

        Parameters:
        ----------
        scribe: Scribe object
            Object from Scribe class which holds all data summary and
            processing information.

        '''
        # start with empty dict which will hold node information
        self.nodes = {}
        # list of nodes relating to preprocessing steps
        self.preprocessing_nodes = []
        # Scribe object for accessing information for output
        self.scribe = scribe

    def get_nodes(self):
        '''
        Creates the nodes required to produce a graphviz workflow image.

        '''
        # 1. create node for dataset -  first step
        self.nodes['1'] = ['1', self.scribe.dataset_name, '#fcfcfc',
                           'rounded, solid']
        # 2. create node for every different preprocessing method used
        # 2.1 imputed missing values
        if self.scribe.preprocessing.check_imputes_step() is True:
            self.nodes['2.1'] = ['2.1', 'Imputed missing values', '#4affc0',
                                 'rounded, filled']
            self.preprocessing_nodes.append('2.1')
        # 2.2 encoded non-numeric fields
        if self.scribe.preprocessing.check_dummy_encoding() is True:
            self.nodes['2.2'] = ['2.2', 'Encoded non-numeric fields',
                                 '#4affc0', 'rounded, filled']
            self.preprocessing_nodes.append('2.2')

        # 2.3 scaled ordered categorical fields
        if self.scribe.preprocessing.check_cats_scaled() is True:
            self.nodes['2.3'] = ['2.3', 'Scaled ordered categorical fields',
                                 '#4affc0', 'rounded, filled']
            self.preprocessing_nodes.append('2.3')

        # 3. Model chosen - return True if there is one
        if self.scribe.model.check_model_exists() is True:
            self.get_model_nodes()
            return True
        else:
            return False

    def create_workflow_image(self, workflow_title="model workflow"):
        '''
        Creates workflow image

        Parameters:
        ----------
        scribe: class
            class which holds workflow information

        '''
        # if no model has been processed yet through package
        if self.get_nodes() is False:
            # print message to advise
            print('Unable to make a workflow yet.')
        else:
            # add the location of the image file to visuals_loc
            # attribute of Scribe object
            img_folder = f'{self.scribe.dir}/images'
            # if image folder doesn't exist, create it
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            # create file name
            file_name = f'{img_folder}/{workflow_title}'

            # create the initial graph
            dot = graphviz.Digraph(workflow_title,
                                   filename=file_name,
                                   node_attr={'fontsize': '12',
                                              'fontname': 'Arial Black',
                                              'shape': 'rectangle'},
                                   format='png')
            # add title to workflow
            dot.attr(labelloc='t', fontsize='20', fontname='Arial Black',
                     label=workflow_title)
            # compound required for subclasses
            dot.attr(compound='true')

            # loop through nodes in Scribe object to create
            for k, v in self.nodes.items():
                dot.node(v[0], v[1], fillcolor=v[2], style=v[3])

            # if preprocessing list not empty
            edges = []
            # variable for when there is more than one preprocessing
            # stage to include
            prep_edges = None
            # if there are nodes in the preprocessing list
            if self.preprocessing_nodes != []:
                # first edge is always connecting '1' data to first node
                # in list
                first_edge = ['1', self.preprocessing_nodes[0]]
                # add adge to edges list
                edges.append(first_edge)
                # if there is only one node in the preprocessing list
                # and '3.1' is in the main node dictionary (the node
                # reference for if there is a model)
                if (len(self.preprocessing_nodes) == 1
                   and '3.1' in self.nodes.keys()):
                    # create edge between only preprocessing item and
                    # the model node
                    edge = [self.preprocessing_nodes[0], '3.1']
                    # add edge to edges list
                    edges.append(edge)
                # if more than one item in preprocessing list
                else:
                    # create a list of lists showing how they will
                    # sequentially join as edges
                    prep_edges = [[self.preprocessing_nodes[i],
                                  self.preprocessing_nodes[i + 1]] for i
                                  in range(len(self.preprocessing_nodes)
                                           - 1)]
                    # if node name for model is in nodes dictionary
                    if '3.1' in self.nodes.keys():
                        # join final preprocessing node to model as an
                        # edge
                        edge = [self.preprocessing_nodes[-1], '3.1']
                        # add edge to edges list
                        edges.append(edge)
            # if there are no preprocessing steps
            else:
                # if model node in nodes dictionary
                if '3.1' in self.nodes.keys():
                    # create edge connecting data '1' to model '3.1'
                    edge = ('1', '3.1')
                    # add edge to edges list
                    edges.append(edge)

            # model selection - more options would be added here if
            # package expanded to other models/variations

            # if logistic regression model using GridCV search / skfold
            if self.scribe.model.model_type == 'LR_GCV_skf':
                # if there is more than one preprocessing stage in log
                if prep_edges is not None:
                    # create a subgraph for preprocessing
                    with dot.subgraph(name='cluster0') as c:
                        c.attr(style='filled', color='lightgrey', rank='same')
                        c.node_attr.update(style='filled', color='white')
                        # edges connecting preprocesses together here
                        c.edges(prep_edges)
                        # title to display for preprocessing cluster
                        c.attr(label='Preprocess Data')
                        c.attr(constraint='false')
                # add a subgraph for the GridCV search element
                with dot.subgraph(name='cluster1') as c:
                    c.attr(style='filled', color='lightgrey')
                    c.edges([('4.1', '4.2')])
                    c.attr(label='Grid CV Search')
                    c.attr(constraint='false')
                # if there is more than one preprocessing step
                if prep_edges is not None:
                    # join first edge arrow to 'cluster0' subgraph
                    dot.edge(edges[0][0], edges[0][1], lhead='cluster0')
                    # iterate edges between first and last if applicable
                    for i in edges[1:-1]:
                        dot.edge(i[0], i[1])
                    # create edge from preprocessing to model so the
                    # arrow comes from edge of subgraph not node
                    dot.edge(edges[-1][0], edges[-1][1], ltail='cluster0')
                # if only one or no preprocessing steps
                else:
                    # iterate through edges list of lists and create
                    for a, b in edges:
                        dot.edge(a, b)
                # edges to create specific model
                dot.edge('3.1', '4.2', lhead='cluster1',
                         taillabel='Training Data')
                dot.edge('3.1', '4.3')
                dot.edge('4.2', '4.3', ltail='cluster1',
                         taillabel='Best models', weight='1')
                dot.edge('4.3', '5.1')
                # add more graph presentation options
                # 'ortho'= rect lines, rankdir=top-bottom
                dot.attr(splines='ortho', rankdir='TB', rank='source',
                         style='circo')

                # create the .png image file and clean up code file
                dot.render(view=False, cleanup=True).replace('\\', '/')

                # store file path in visuals_loc attribute of Scribe
                self.scribe.visuals_loc['workflow'] = f"{file_name}.png"

            # otherwise, advise no applicable model
            else:
                print('No applicable model selected for worklow.')
                # clear out nodes attribute
                self.nodes = {}

    def get_model_nodes(self):
        '''
        retrieves model node shape based on model type.

        If successful, returns True.  If unsuccessful, returns False.

        Returns:
        -------
        boolean
        '''
        # If package updated with more models, if statement would
        # be expanded.
        # Model: LR GridSearchCV with Stratified K fold Cross Validation
        if self.scribe.model.model_type == 'LR_GCV_skf':
            # format train and test splits for nodes
            train_split = "{:.0%}".format(self.scribe.model.split)
            test_dec = 1 - self.scribe.model.split
            test_split = "{:.0%}".format(test_dec)
            # add following nodes to model
            self.nodes['3.1'] = ['3.1', f'Repeated stratified\nKCV\n'
                                 f'(folds={self.scribe.model.k_num})',
                                 '#fcfcfc', 'rounded, solid']
            self.nodes['4.1'] = ['4.1', 'Hyperparameters', '#fcfcfc',
                                 'rounded, solid']
            self.nodes['4.2'] = ['4.2', f'Training ({train_split})',
                                 '#fcfcfc', 'rounded, solid']
            self.nodes['4.3'] = ['4.3', f'Testing ({test_split})',
                                 '#fcfcfc', 'rounded, solid']
            self.nodes['5.1'] = ['5.1', 'Performance and\nEvaluation',
                                 '#fcfcfc', 'rounded, solid']
            # return True as model retrieved and added
            return True

        # if no model selected, return False
        return False
