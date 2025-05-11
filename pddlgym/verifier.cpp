#include <iostream>

#include "verifier.hpp"


void verifier::initialiseNDTG()
{
    _NDTG.BuildDTGs();
    _NDTG_initialised=true;
}


bool verifier::verify_NDTG_step(const SAS_State& curr, const SAS_State& prev, SAS_Assignment &waitfor)
{
    //unreachability check
    if (_NDTG.unreachable(curr.get_assignment(),prev.get_assignment())){_reason="Unreachability case"; return false;}

    SAS_State prev_temp(prev);

    bool any_different;

    //initially check the different variables and check Lemma 4
    do{
    any_different=false;
    for (auto fact : curr.get_assignment()){
        //variable not "touched" by "previous state" or with the same values (these are unimportant at this stage)
        if (!prev_temp.get_assignment().contains(fact.first)||prev_temp.get(fact.first)==fact.second) continue;
            bool lemma4_satisfied=true;
            //std::cout << "Processing variable... " << _problem.get_variables()[fact.first].to_strips_string_atom(fact.second) << std::endl;
            //using Lemma 4 (greedily find a path from curr to prev_temp)
            if (_NDTG.isLeaf(fact.first,fact.second)&&_NDTG.isPath(fact.first,prev_temp.get(fact.first),fact.second)){
                SAS_State s(curr.get_assignment());
                std::deque<SAS_Operator> events;
                while (s.get(fact.first)!=prev_temp.get(fact.first)){
                    //greedily find a sequence of events forming the path..
                    bool event_selected = false;
                    for (auto ev : _problem.get_events()) if (ev.get_minimal_effects().satisfy(fact.first,s.get(fact.first))&&
                                                              !_NDTG.unreachable(ev.get_preconditions(),prev_temp.get_assignment())&&
                                                              //s.is_regressively_applicable(ev)&&
                                                          (!(ev.get_preconditions().contains(fact.first))||_NDTG.isPath(fact.first,prev_temp.get(fact.first), ev.get_preconditions().get(fact.first)||prev_temp.get(fact.first)==ev.get_preconditions().get(fact.first)))
                                                              )
                    {
                        //checks from condition (iii) of Lemma 4
                        if (!events.empty() && events.front().get_preconditions().satisfied_by(ev.get_minimal_effects())){
                            bool no_clobberer=true;
                            for (auto ev2 : _problem.get_events()) if (ev2.get_name()!=ev.get_name()) {
                                if (ev2.isClobbererFor(ev)&&!_NDTG.unreachable(ev2.get_preconditions(),prev_temp.get_assignment())&&(!ev2.get_preconditions().contains(fact.first)||ev2.get_preconditions().get(fact.first)==ev.get_preconditions().get(fact.first))) {no_clobberer=false;break;}
                            }
                            if (!no_clobberer) continue;
                        }
                        //now we have (greedily) selected the event
                       event_selected=true;
                       s.regressivlvely_apply(ev);
                       events.push_front(ev);

                       //std::cout << ev.get_name() << " ";
                    }
                    if (!event_selected){_reason="Lemma 4 failed on fact "+_problem.get_variables()[fact.first].get_value(fact.second); return false;}
                }

                //std::cout << std::endl;
                // compare s with prev_temp


                bool match_check=true;
                for (auto f : events.front().get_preconditions()) if (prev_temp.get_assignment().contains(f.first)&&f.second!=prev_temp.get(f.first)){match_check=false;break;}
                if (!match_check) {lemma4_satisfied=false; _reason="Lemma 4 failed on fact "+_problem.get_variables()[fact.first].get_value(fact.second); return false;}

                //add waitfor
                for (auto f : s.get_assignment()) if (!prev_temp.get_assignment().contains(f.first)) waitfor.set(f.first,f.second);

                //apply events
                //std::cout << "Applying events acc to Lemma 4 - ";
                for (auto e : events) {prev_temp.apply(e.get_minimal_effects());}// std::cout << e.get_name() << " ";}
                //std::cout << std::endl;

                any_different=true;
                break;
            } else lemma4_satisfied=false;

            if (!lemma4_satisfied){ return false;}

    }
    } while (any_different);


            //std::cout << " state to process after Lemma 4 " << " - ";
            //    for (auto atom : prev_temp.get_assignment()) std::cout << _problem.get_variables()[atom.first].to_strips_string_atom(atom.second);
            //std::cout << std::endl;

    //iterate over facts from the "current state" and apply Lemmas to "connect" with "previous state"
    bool lemma3_used=false;
    for (auto fact : curr.get_assignment()){

        //variable not "touched" by "previous state"
        //if (!prev_temp.get_assignment().contains(fact.first)) continue;

        //cases in which the value of the variable is the same as in the "prev" state
        if (!prev_temp.get_assignment().contains(fact.first) || fact.second==prev_temp.get(fact.first)){
            //using Lemma 1
            if (_NDTG.isLeaf(fact.first,fact.second)) continue;

            //using Lemma 2
            bool passed_lemma2 = true;
            for (auto ev : _problem.get_events()) if (ev.deletesFact(fact.first,fact.second)){
                if (!_NDTG.unreachable(ev.get_preconditions(),prev_temp.get_assignment())){
                    //the harder part
                    bool invalidated_precondition=false;
                    for (auto pre : ev.get_preconditions()) if (!prev_temp.get_assignment().contains(pre.first)){
                        //try to get a leaf node invalidating pre
                        std::vector<size_t> leaves=_NDTG.leavesOF(pre.first,pre.second);
                        if (leaves.size()==1){
                            waitfor.set(pre.first,leaves[0]);
                            invalidated_precondition=true;
                            break;
                        }
                    }
                    if (!invalidated_precondition){ passed_lemma2=false;break;}
                }
            }
            if (passed_lemma2) continue;

            //using Lemma 3
            if (!lemma3_used){
                bool passed_lemma3 = true;
                for (auto ev : _problem.get_events()) if (ev.deletesFact(fact.first,fact.second)){
                    for (auto ev2 : _problem.get_events()) if (ev.hold_after().satisfy_all(ev2.get_preconditions())){
                        for (auto ev3 : _problem.get_events()) if (ev2.get_name()!=ev3.get_name()&&ev3.isClobbererFor(ev2)&&!ev2.get_preconditions().any_mismatch(ev3.get_preconditions())){
                            if ((!ev3.get_preconditions().contains(fact.first)||ev3.get_preconditions().get(fact.first)!=fact.second)&&(!ev3.get_minimal_effects().contains(fact.first)||ev3.get_minimal_effects().get(fact.first)!=fact.second)){
                            //if (ev3.get_preconditions().get(fact.first)!=fact.second&&ev3.get_minimal_effects().get(fact.first)!=fact.second){
                                //it's bad, the assumption of Lemma 3 not satisfied
                                //std::cout << "Failing Lemma 3 on event " << ev2.get_name() << " by event " << ev3.get_name() << std::endl;
                                passed_lemma3=false;
                                break;
                            }
                        }
                        if (!passed_lemma3) break;
                    }
                    if (!passed_lemma3) break;
                }
                if (passed_lemma3) {lemma3_used=true;continue;}
            }
        }
        //we finished all check but did not find any "connection"
        _reason="Failed on fact "+_problem.get_variables()[fact.first].get_value(fact.second);
        return false;
    }

    return true;
}


bool verifier::verify_NDTG()
{

    if (!_NDTG_initialised) initialiseNDTG();

    //_NDTG.outputDTGInfo();

    SAS_State current_state=_problem.get_goal();
    //for (int i=_plan.get_length()-1;i>=0;i--){
    for (auto current_op_it=_plan.rbegin();current_op_it!=_plan.rend();current_op_it++){
            //auto current_op=current_op_it->get();
            int i=_plan.get_length();

            //do the checks
            //std::cout << " state to process for action " << current_op_it->get().get_name() << " - ";
            //    for (auto atom : current_state.get_assignment()) std::cout << _problem.get_variables()[atom.first].to_strips_string_atom(atom.second);
            //std::cout << std::endl;

            SAS_Assignment *waitfor=new SAS_Assignment();
            bool check=verify_NDTG_step(current_state, current_op_it->get().hold_after(true),*waitfor);
            if (!check){_step=i; return false;}
            current_op_it->get().set_waitfor(*waitfor);

            current_state.regressivlvely_apply(current_op_it->get(),true);

            //std::cout << " new waitfor for action " << current_op_it->get().get_name() << " - ";
            //    for (auto atom : current_op_it->get().get_waitfor()) std::cout << _problem.get_variables()[atom.first].to_strips_string_atom(atom.second);
            //std::cout << std::endl;

            i--;
    }

    //do the check with the initial state
    SAS_Assignment initial_waitfor;

    //std::cout << " state to process for the initial state - ";
    //        for (auto atom : current_state.get_assignment()) std::cout << _problem.get_variables()[atom.first].to_strips_string_atom(atom.second);
   //std::cout << std::endl;

    bool check=verify_NDTG_step(current_state, _problem.get_init(),initial_waitfor);
    if (!check){_step=-1; return false;}

    return true;
}