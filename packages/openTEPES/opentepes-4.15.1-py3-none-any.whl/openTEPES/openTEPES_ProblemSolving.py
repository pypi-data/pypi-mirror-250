"""
Open Generation, Storage, and Transmission Operation and Expansion Planning Model with RES and ESS (openTEPES) - January 06, 2024
"""

import time
import os
import pandas        as pd
import pyomo.environ as pyo
import psutil
import logging
from   pyomo.opt             import SolverFactory, SolverStatus, TerminationCondition
from   pyomo.util.infeasible import log_infeasible_constraints
from   pyomo.environ         import Suffix

def ProblemSolving(DirName, CaseName, SolverName, OptModel, mTEPES, pIndLogConsole, p, sc):
    print('Problem solving                        ****')
    _path = os.path.join(DirName, CaseName)
    StartTime = time.time()

    #%% solving the problem
    Solver = SolverFactory(SolverName)                                                       # select solver
    if SolverName == 'gurobi':
        Solver.options['LogFile'       ] = _path+'/openTEPES_gurobi_'+CaseName+'.log'
        # Solver.options['IISFile'     ] = _path+'/openTEPES_gurobi_'+CaseName+'.ilp'        # should be uncommented to show results of IIS
        Solver.options['Method'        ] = 2                                                 # barrier method
        # Solver.options['MIPFocus'      ] = 3
        # Solver.options['Presolve'      ] = 2
        # Solver.options['RINS'          ] = 100
        Solver.options['Crossover'     ] = -1
        # Solver.options['BarConvTol'    ] = 1e-9
        # Solver.options['BarQCPConvTol' ] = 0.025
        Solver.options['MIPGap'        ] = 0.01
        Solver.options['Threads'       ] = int((psutil.cpu_count(logical=True) + psutil.cpu_count(logical=False))/2)
        Solver.options['TimeLimit'     ] =    36000
        Solver.options['IterationLimit'] = 36000000
    if SolverName == 'gams':
        solver_options = {
            'file COPT / cplex.opt / ; put COPT putclose "LPMethod 4" / "RINSHeur 100" / ; GAMS_MODEL.OptFile = 1 ;'
            'option SysOut  = off   ;',
            'option LP      = cplex ; option MIP     = cplex    ;',
            'option ResLim  = 36000 ; option IterLim = 36000000 ;',
            'option Threads = '+str(int((psutil.cpu_count(logical=True) + psutil.cpu_count(logical=False))/2))+' ;'
        }

    if (mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc) + mTEPES.pIndBinGenRetire()*len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd) + mTEPES.pIndBinNetInvest ()*len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc) + mTEPES.pIndBinNetH2Invest()*len(mTEPES.pc)*sum(mTEPES.pIndBinPipeInvest[pc] for pc in mTEPES.pc) +
        mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr) +                                                                                                  mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la) + len(mTEPES.g2g) == 0 or
        ((len(mTEPES.gc) == 0 or (len(mTEPES.gc) > 0 and mTEPES.pIndBinGenInvest() == 2)) and (len(mTEPES.gd) == 0 or (len(mTEPES.gd) > 0 and mTEPES.pIndBinGenRetire() == 2)) and (len(mTEPES.lc) == 0 or (len(mTEPES.lc) > 0 and mTEPES.pIndBinNetInvest () == 2)) and (len(mTEPES.pc) == 0 or (len(mTEPES.pc) > 0 and mTEPES.pIndBinNeH2tInvest() == 2)) and
         (len(mTEPES.nr) == 0 or (len(mTEPES.nr) > 0 and mTEPES.pIndBinGenOperat() == 0)) and                                                                                      (len(mTEPES.la) == 0 or (len(mTEPES.la) > 0 and mTEPES.pIndBinLineCommit() == 0)))):
        # there are no binary decisions (no investment/retirement decisions or investment/retirement decisions already ignored, no line switching/unit commitment, no mutually exclusive units)
        if mTEPES.p.ord(p)*mTEPES.sc.ord(sc) == 1:
            OptModel.dual = Suffix(direction=Suffix.IMPORT_EXPORT)
            OptModel.rc   = Suffix(direction=Suffix.IMPORT_EXPORT)

    if SolverName == 'gurobi':
        SolverResults = Solver.solve(OptModel, tee=True, report_timing=True)
    if SolverName == 'gams'  :
        SolverResults = Solver.solve(OptModel, tee=True, report_timing=True, symbolic_solver_labels=False, add_options=solver_options)

    print('Termination condition: ', SolverResults.solver.termination_condition)
    if SolverResults.solver.termination_condition == TerminationCondition.infeasible:
        log_infeasible_constraints(OptModel, log_expression=True, log_variables=True)
        logging.basicConfig(filename=_path+'/openTEPES_infeasibilities_'+CaseName+'.txt', level=logging.INFO)
    assert (SolverResults.solver.termination_condition == TerminationCondition.optimal or SolverResults.solver.termination_condition == TerminationCondition.maxTimeLimit or SolverResults.solver.termination_condition == TerminationCondition.infeasible.maxIterations), 'Problem infeasible'
    SolverResults.write()                                                              # summary of the solver results

    #%% fix values of some variables to get duals and solve it again
    # binary/continuous investment decisions are fixed to their optimal values
    # binary            operation  decisions are fixed to their optimal values
    if (mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc) + mTEPES.pIndBinGenRetire()*len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd) + mTEPES.pIndBinNetInvest ()*len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc) + mTEPES.pIndBinNetH2Invest()*len(mTEPES.pc)*sum(mTEPES.pIndBinPipeInvest[pc] for pc in mTEPES.pc) +
        mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr) +                                                                                                  mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la) + len(mTEPES.g2g) > 0 and
        ((len(mTEPES.gc) > 0 and mTEPES.pIndBinGenInvest() != 2) or (len(mTEPES.gd) > 0 and mTEPES.pIndBinGenRetire() != 2) or (len(mTEPES.lc) > 0 and mTEPES.pIndBinNetInvest () != 2) or (len(mTEPES.pc) > 0 and mTEPES.pIndBinNetH2Invest() != 2) or
         (len(mTEPES.nr) > 0 and mTEPES.pIndBinGenOperat() == 0) or                                                            (len(mTEPES.la) > 0 and mTEPES.pIndBinLineCommit() == 0))):
        if mTEPES.pIndBinGenInvest()*len(mTEPES.gc)*sum(mTEPES.pIndBinUnitInvest[gc] for gc in mTEPES.gc):
            for gc in mTEPES.gc:
                if mTEPES.pIndBinUnitInvest[gc] != 0:
                    OptModel.vGenerationInvest[p,gc].fix(round(OptModel.vGenerationInvest[p,gc]()))
                else:
                    OptModel.vGenerationInvest[p,gc].fix(      OptModel.vGenerationInvest[p,gc]())
        if mTEPES.pIndBinGenRetire()*len(mTEPES.gd)*sum(mTEPES.pIndBinUnitRetire[gd] for gd in mTEPES.gd):
            for gd in mTEPES.gd:
                if mTEPES.pIndBinUnitRetire[gd] != 0:
                    OptModel.vGenerationRetire[p,gd].fix(round(OptModel.vGenerationRetire[p,gd]()))
                else:
                    OptModel.vGenerationRetire[p,gd].fix(      OptModel.vGenerationRetire[p,gd]())
        if mTEPES.pIndHydroTopology == 1:
            if mTEPES.pIndBinRsrInvest()*len(mTEPES.rn)*sum(mTEPES.pIndBinRsrvInvest[gc] for rc in mTEPES.rn):
                for rc in mTEPES.rn:
                    if mTEPES.pIndBinRsrvInvest[gc] != 0:
                        OptModel.vReservoirInvest[p,rc].fix(round(OptModel.vReservoirInvest[p,rc]()))
                    else:
                        OptModel.vReservoirInvest[p,rc].fix(      OptModel.vReservoirInvest[p,rc]())
        if mTEPES.pIndBinNetInvest()*len(mTEPES.lc)*sum(mTEPES.pIndBinLineInvest[lc] for lc in mTEPES.lc):
            for ni,nf,cc in mTEPES.lc:
                if mTEPES.pIndBinLineInvest[  ni,nf,cc] != 0:
                    OptModel.vNetworkInvest[p,ni,nf,cc].fix(round(OptModel.vNetworkInvest[p,ni,nf,cc]()))
                else:
                    OptModel.vNetworkInvest[p,ni,nf,cc].fix(      OptModel.vNetworkInvest[p,ni,nf,cc]())
        if mTEPES.pIndHydrogen == 1:
            if mTEPES.pIndBinNetH2Invest()*len(mTEPES.pc)*sum(mTEPES.pIndBinPipeInvest[pc] for pc in mTEPES.pc):
                for ni,nf,cc in mTEPES.pc:
                    if mTEPES.pIndBinPipeInvest [  ni,nf,cc] != 0:
                        OptModel.vPipelineInvest[p,ni,nf,cc].fix(round(OptModel.vPipelineInvest[p,ni,nf,cc]()))
                    else:
                        OptModel.vPipelineInvest[p,ni,nf,cc].fix(      OptModel.vPipelineInvest[p,ni,nf,cc]())
        if mTEPES.pIndBinGenOperat()*len(mTEPES.nr)*sum(mTEPES.pIndBinUnitCommit[nr] for nr in mTEPES.nr):
            for n,nr in mTEPES.n*mTEPES.nr:
                if mTEPES.pIndBinUnitCommit[nr] != 0:
                    OptModel.vCommitment[p,sc,n,nr].fix(round(OptModel.vCommitment[p,sc,n,nr]()))
                    OptModel.vStartUp   [p,sc,n,nr].fix(round(OptModel.vStartUp   [p,sc,n,nr]()))
                    OptModel.vShutDown  [p,sc,n,nr].fix(round(OptModel.vShutDown  [p,sc,n,nr]()))
        if mTEPES.pIndBinLineCommit()*len(mTEPES.la)*sum(mTEPES.pIndBinLineSwitch[la] for la in mTEPES.la):
            for n,ni,nf,cc in mTEPES.n*mTEPES.la:
                if mTEPES.pIndBinLineSwitch[ni,nf,cc] != 0:
                    OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(round(OptModel.vLineCommit   [p,sc,n,ni,nf,cc]()))
                    OptModel.vLineOnState [p,sc,n,ni,nf,cc].fix(round(OptModel.vLineOnState  [p,sc,n,ni,nf,cc]()))
                    OptModel.vLineOffState[p,sc,n,ni,nf,cc].fix(round(OptModel.vLineOffState [p,sc,n,ni,nf,cc]()))
                elif (ni,nf,cc) in mTEPES.lc:
                    OptModel.vLineCommit  [p,sc,n,ni,nf,cc].fix(round(OptModel.vNetworkInvest[p,     ni,nf,cc]()))
        if len(mTEPES.g2g):
            for nr in mTEPES.nr:
                if sum(1 for g in mTEPES.nr if (nr,g) in mTEPES.g2g or (g,nr) in mTEPES.g2g):
                    OptModel.vMaxCommitment[nr].fix(round(OptModel.vMaxCommitment[nr]()))

        if mTEPES.p.last() == mTEPES.pp.last() and mTEPES.sc.last() == mTEPES.scc.last() and mTEPES.st.last() == mTEPES.stt.last():
            OptModel.dual = Suffix(direction=Suffix.IMPORT_EXPORT)
            OptModel.rc   = Suffix(direction=Suffix.IMPORT_EXPORT)

        SolverResults = Solver.solve(OptModel, tee=True, report_timing=True)

    # saving the dual variables for writing in output results
    pDuals = {}
    for c in OptModel.component_objects(pyo.Constraint, active=True):
        if c.is_indexed():
            for index in c:
                pDuals[str(c.name)+str(index)] = OptModel.dual[c[index]]

    mTEPES.pDuals.update(pDuals)

    SolvingTime = time.time() - StartTime

    print('***** Period: '+str(p)+', Scenario: '+str(sc)+' ******')
    print    ('  Problem size                         ... ', OptModel.model().nconstraints(), 'constraints, ', OptModel.model().nvariables()-mTEPES.nFixedVariables+1, 'variables')
    print    ('  Solution time                        ... ', round(SolvingTime), 's')
    print    ('  Total system                 cost [MEUR] ', OptModel.vTotalSCost())
    print    ('  Total generation  investment cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pGenInvestCost [gc      ]   * OptModel.vGenerationInvest[p,gc      ]() for gc       in mTEPES.gc))
    print    ('  Total generation  retirement cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pGenRetireCost [gd      ]   * OptModel.vGenerationRetire[p,gd      ]() for gd       in mTEPES.gd))
    if mTEPES.pIndHydroTopology == 1 and len(mTEPES.rn):
        print('  Total reservoir   investment cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pRsrInvestCost [rc      ]   * OptModel.vReservoirInvest [p,rc      ]() for rc       in mTEPES.rn))
    else:
        print('  Total reservoir   investment cost [MEUR] ', 0.0)
    print    ('  Total network     investment cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pNetFixedCost  [ni,nf,cc]   * OptModel.vNetworkInvest   [p,ni,nf,cc]() for ni,nf,cc in mTEPES.lc))
    if mTEPES.pIndHydrogen      == 1 and len(mTEPES.pc):
        print('  Total pipeline    investment cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pLineInvestCost[ni,nf,cc]   * OptModel.vPipelineInvest  [p,ni,nf,cc]() for ni,nf,cc in mTEPES.pc))
    else:
        print('  Total pipeline    investment cost [MEUR] ', 0.0)
    print    ('  Total generation  operation  cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pScenProb      [p,sc    ]() * OptModel.vTotalGCost      [p,sc,n    ]() for n        in mTEPES.n ))
    print    ('  Total consumption operation  cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pScenProb      [p,sc    ]() * OptModel.vTotalCCost      [p,sc,n    ]() for n        in mTEPES.n ))
    print    ('  Total emission               cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pScenProb      [p,sc    ]() * OptModel.vTotalECost      [p,sc,n    ]() for n        in mTEPES.n ))
    print    ('  Total reliability            cost [MEUR] ', sum(mTEPES.pDiscountedWeight[p] * mTEPES.pScenProb      [p,sc    ]() * OptModel.vTotalRCost      [p,sc,n    ]() for n        in mTEPES.n ))
