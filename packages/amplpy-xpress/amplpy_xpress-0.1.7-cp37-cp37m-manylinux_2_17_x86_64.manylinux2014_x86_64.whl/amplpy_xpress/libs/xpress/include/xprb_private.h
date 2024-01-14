/* * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                 */
/* Copyright (C) 2018-2023 Fair Isaac Corporation  */
/*                            All rights reserved  */
/*                                                 */
/* * * * * * * * * * * * * * * * * * * * * * * * * */

// Private XPRB functions only used by C++, Java and .Net BCL

#ifndef _XPRB_PRIVATE
#define _XPRB_PRIVATE

#if defined(_WIN32) || defined(_WIN64)
#define XB_CC __stdcall
#ifdef _FILE_DEFINED
#define _STDIO_H
#endif
#define XB_EXTERN extern __declspec(dllimport)
#else
#define XB_CC
#if defined(_STDIO_INCLUDED) || defined (_H_STDIO)
#define _STDIO_H
#endif
#define XB_EXTERN extern
#endif

#ifndef XPRS_EXPORT
#  define XPRS_EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

XPRS_EXPORT int XB_CC XPRBaddexpr(struct Xbexpr *e1, struct Xbexpr *e2);
XPRS_EXPORT int XB_CC XPRBaddexpr_term(struct Xbexpr *e, struct Xbvar *var1, struct Xbvar *var2, double d);
XPRS_EXPORT int XB_CC XPRBappctr(struct Xbctr *lctr, struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBappsos(struct Xbsos *sos, struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBappcut(struct Xbcut *cut, struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBassignexpr(struct Xbexpr *e1, struct Xbexpr *e2);
XPRS_EXPORT int XB_CC XPRBsetcut(struct Xbcut *cut, struct Xbexpr *e, int type);
XPRS_EXPORT void XB_CC XPRBchsexpr(struct Xbexpr *e);
XPRS_EXPORT void XB_CC XPRBclearexpr(struct Xbexpr *e);
XPRS_EXPORT void XB_CC XPRBdelexpr(struct Xbexpr *e);
XPRS_EXPORT double XB_CC XPRBevalexpr(struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBslinitj(void);
XPRS_EXPORT void XB_CC XPRBmulcexpr(struct Xbexpr *e,double d);
XPRS_EXPORT int XB_CC XPRBmulexpr(struct Xbexpr *e1,struct Xbexpr *e2);
XPRS_EXPORT int XB_CC XPRBsetobjexpr(struct Xbprob *prob, struct Xbexpr *obj);
XPRS_EXPORT int XB_CC XPRBsetsos(struct Xbsos *sos, struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBsetctr(struct Xbctr *lct, struct Xbexpr *e, int type);
XPRS_EXPORT int XB_CC XPRBsetexpr_term(struct Xbexpr *e, struct Xbvar *var1, struct Xbvar *var2, double d);
XPRS_EXPORT int XB_CC XPRBprintexpr(struct Xbprob *prob, struct Xbexpr *e, int type, double range);
XPRS_EXPORT int XB_CC XPRBdelprob_jprobdelxp(struct Xbprob *prob);
XPRS_EXPORT int XB_CC XPRBdelprob_jprob(struct Xbprob *prob);
XPRS_EXPORT struct Xbexpr * XB_CC XPRBnewexpr(double d, struct Xbvar *var1, struct Xbvar *var2);
XPRS_EXPORT int XB_CC XPRBgetstatexpr(struct Xbexpr *e);
XPRS_EXPORT int XB_CC XPRBgetvarstat(struct Xbvar *v);
XPRS_EXPORT int XB_CC XPRBdupexpr(struct Xbexpr **e_d, struct Xbexpr *e_s);
XPRS_EXPORT char * XB_CC Xbexpr2str(struct Xbexpr *e, int type);
XPRS_EXPORT void XB_CC XPRBfree2str(char *p);
XPRS_EXPORT int XB_CC XPRBsetsolvar(struct Xbsol *sol, struct Xbvar *var, double val);
XPRS_EXPORT char * XB_CC XPRBexpr2str(struct Xbexpr *e, int type);

#define xbaddexpr XPRBaddexpr
#define xbaddexpr_term XPRBaddexpr_term
#define xbappctr XPRBappctr
#define xbappsos XPRBappsos
#define xbappcut XPRBappcut
#define xbassignexpr XPRBassignexpr
#define xbsetcut XPRBsetcut
#define xbchsexpr XPRBchsexpr
#define xbclearexpr XPRBclearexpr
#define xbdelexpr XPRBdelexpr
#define xbevalexpr XPRBevalexpr
#define xbslinitj XPRBslinitj
#define xbmulcexpr XPRBmulcexpr
#define xbmulexpr XPRBmulexpr
#define xbsetobjexpr XPRBsetobjexpr
#define xbsetsos XPRBsetsos
#define xbsetctr XPRBsetctr
#define xbsetexpr_term XPRBsetexpr_term
#define xbprintexpr XPRBprintexpr
#define xbdelprob_jprob XPRBdelprob_jprob
#define xbnewexpr XPRBnewexpr
#define xbgetstatexpr XPRBgetstatexpr
#define xbgetvarstat XPRBgetvarstat
#define xbdupexpr XPRBdupexpr
#define xbexpr2str XPRBexpr2str
#define xbfree2str XPRBfree2str

#ifdef __cplusplus
}
#endif

#endif
