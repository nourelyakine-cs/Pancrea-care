(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/app/login/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>AuthPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/image.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/framer-motion/dist/es/render/components/motion/proxy.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$components$2f$AnimatePresence$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/framer-motion/dist/es/components/AnimatePresence/index.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/lib/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$components$2f$PasswordRequirements$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/components/PasswordRequirements.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$about$2d$doctors$2e$png$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$assets$2f$about$2d$doctors$2e$png__$28$static__in__ecmascript$2c$__tag__client$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object__with__data__url$2c$__ecmascript$29$__ = __turbopack_context__.i('[project]/assets/about-doctors.png.mjs { IMAGE => "[project]/assets/about-doctors.png (static in ecmascript, tag client)" } [app-client] (structured image object with data url, ecmascript)');
var __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$logo$2e$png$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$assets$2f$logo$2e$png__$28$static__in__ecmascript$2c$__tag__client$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object__with__data__url$2c$__ecmascript$29$__ = __turbopack_context__.i('[project]/assets/logo.png.mjs { IMAGE => "[project]/assets/logo.png (static in ecmascript, tag client)" } [app-client] (structured image object with data url, ecmascript)');
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
;
;
;
;
;
/** Espace correspondant au rôle : c'est le compte connecté qui décide, pas
 *  l'écran d'où l'on arrive. Un médecin ne peut donc pas atterrir sur /admin
 *  et un super admin ne reste pas bloqué sur la liste des patients. */ function espacePour(compte) {
    return compte.role === "super_admin" ? "/admin" : "/dashboard";
}
function AuthPageContent() {
    _s();
    const searchParams = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSearchParams"])();
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"])();
    const [isSignUp, setIsSignUp] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        "AuthPageContent.useState": ()=>searchParams.get("mode") === "signup"
    }["AuthPageContent.useState"]);
    const [isExiting, setIsExiting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [awaitingValidation, setAwaitingValidation] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [nom, setNom] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [prenom, setPrenom] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [telephone, setTelephone] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [hopital, setHopital] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [email, setEmail] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [password, setPassword] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    // La garde d'accès renvoie ici avec `?motif=profil-absent` quand la session est
    // valide mais sans profil clinique. Sans ce message, l'utilisateur rejoue sa
    // connexion et repart au même endroit sans jamais comprendre d'où vient le
    // renvoi. Message initialisé une seule fois : il dépend de la redirection,
    // pas de la saisie.
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        "AuthPageContent.useState": ()=>searchParams.get("motif") === "profil-absent" ? "Votre compte est actif mais pas encore rattaché à un profil clinique. Contactez l'administration de la plateforme pour le rattacher." : ""
    }["AuthPageContent.useState"]);
    const [policy, setPolicy] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    // Les exigences affichées viennent de l'API : c'est exactement ce que le
    // serveur refusera, pas une copie qui pourrait dériver.
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "AuthPageContent.useEffect": ()=>{
            let active = true;
            (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["getPasswordPolicy"])().then({
                "AuthPageContent.useEffect": (p)=>{
                    if (active) setPolicy(p);
                }
            }["AuthPageContent.useEffect"]);
            return ({
                "AuthPageContent.useEffect": ()=>{
                    active = false;
                }
            })["AuthPageContent.useEffect"];
        }
    }["AuthPageContent.useEffect"], []);
    const passwordCompliant = (0, __TURBOPACK__imported__module__$5b$project$5d2f$components$2f$PasswordRequirements$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["isPasswordCompliant"])(password, policy ?? __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["DEFAULT_PASSWORD_POLICY"]);
    const showSignUpPitch = isSignUp;
    const handleSubmit = async (e)=>{
        e.preventDefault();
        if (isSignUp && !passwordCompliant) {
            setError("Le mot de passe ne respecte pas les exigences ci-dessus.");
            return;
        }
        setIsLoading(true);
        setError("");
        try {
            if (isSignUp) {
                const res = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["signup"])({
                    nom,
                    prenom,
                    email,
                    password,
                    telephone,
                    hopital
                });
                // Le compte part en file d'attente : aucun jeton n'est renvoyé, il n'y
                // a donc rien à mémoriser ici. On affiche ce que va devenir la
                // connexion au lieu de basculer sur un formulaire inutile.
                setAwaitingValidation({
                    email,
                    message: res.message
                });
            } else {
                const session = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["login"])(email, password);
                localStorage.setItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TOKEN_KEY"], session.access_token);
                router.push(espacePour(session.compte));
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : "Une erreur est survenue.");
        } finally{
            setIsLoading(false);
        }
    };
    const handleBackToHome = (e)=>{
        e.preventDefault();
        setIsExiting(true);
        setTimeout(()=>{
            router.push("/");
        }, 400);
    };
    if (awaitingValidation) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(ValidationPending, {
            email: awaitingValidation.email,
            message: awaitingValidation.message,
            onBack: ()=>{
                setAwaitingValidation(null);
                setIsSignUp(false);
                setError("");
            }
        }, void 0, false, {
            fileName: "[project]/app/login/page.tsx",
            lineNumber: 108,
            columnNumber: 7
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$components$2f$AnimatePresence$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimatePresence"], {
        mode: "wait",
        children: !isExiting && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
            initial: {
                opacity: 0,
                scale: 0.98
            },
            animate: {
                opacity: 1,
                scale: 1
            },
            exit: {
                opacity: 0,
                scale: 0.96,
                y: 15
            },
            transition: {
                duration: 0.4,
                ease: "easeInOut"
            },
            className: "min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 md:p-8 font-serif relative",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                    href: "/",
                    onClick: handleBackToHome,
                    className: "absolute top-6 left-6 z-50",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
                        whileHover: {
                            x: -6
                        },
                        whileTap: {
                            scale: 0.9
                        },
                        transition: {
                            type: "spring",
                            stiffness: 400,
                            damping: 25
                        },
                        className: "flex items-center gap-2 text-sm font-semibold text-[#1D7893] hover:text-[#209BBF] transition-colors duration-200 cursor-pointer",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].svg, {
                            className: "w-5 h-5 stroke-current",
                            fill: "none",
                            viewBox: "0 0 24 24",
                            strokeWidth: "2.5",
                            stroke: "currentColor",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                strokeLinecap: "round",
                                strokeLinejoin: "round",
                                d: "M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18"
                            }, void 0, false, {
                                fileName: "[project]/app/login/page.tsx",
                                lineNumber: 149,
                                columnNumber: 17
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 142,
                            columnNumber: 15
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/login/page.tsx",
                        lineNumber: 136,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 131,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: `relative w-full max-w-4xl min-h-[600px] max-h-[90vh] bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row ${isSignUp ? "h-[90vh]" : ""}`,
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
                            initial: {
                                opacity: 0,
                                x: isSignUp ? 50 : -50
                            },
                            animate: {
                                opacity: 1,
                                x: 0
                            },
                            transition: {
                                duration: 0.5,
                                ease: "easeInOut"
                            },
                            className: `w-full md:w-1/2 h-full min-h-0 flex flex-col ${isSignUp ? "md:order-2" : "md:order-1"}`,
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex-1 min-h-0 overflow-y-auto p-6 sm:p-8 md:p-10 flex flex-col",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "max-w-md mx-auto w-full my-auto flex flex-col justify-center",
                                        children: [
                                            !isSignUp && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                                href: "/",
                                                className: "mb-4 flex justify-center",
                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                                    src: __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$logo$2e$png$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$assets$2f$logo$2e$png__$28$static__in__ecmascript$2c$__tag__client$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object__with__data__url$2c$__ecmascript$29$__["default"],
                                                    alt: "PancreaCare",
                                                    width: 150,
                                                    height: 45,
                                                    className: "h-11 w-auto object-contain mx-auto"
                                                }, void 0, false, {
                                                    fileName: "[project]/app/login/page.tsx",
                                                    lineNumber: 175,
                                                    columnNumber: 21
                                                }, this)
                                            }, void 0, false, {
                                                fileName: "[project]/app/login/page.tsx",
                                                lineNumber: 174,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "mb-5 text-center w-full",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                                        className: "text-xl sm:text-2xl font-extrabold text-[#1D7893]",
                                                        children: isSignUp ? "Créer un compte Médecin" : "Espace Médecin"
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 187,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-xs text-gray-500 mt-1 leading-relaxed",
                                                        children: isSignUp ? "Rejoignez la plateforme déterministe d'aide à la décision." : "Veuillez vous identifier pour accéder au suivi patient."
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 190,
                                                        columnNumber: 19
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/app/login/page.tsx",
                                                lineNumber: 186,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                                                onSubmit: handleSubmit,
                                                className: "space-y-3 w-full",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$components$2f$AnimatePresence$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimatePresence"], {
                                                        children: isSignUp && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
                                                            initial: {
                                                                opacity: 0,
                                                                height: 0
                                                            },
                                                            animate: {
                                                                opacity: 1,
                                                                height: "auto"
                                                            },
                                                            exit: {
                                                                opacity: 0,
                                                                height: 0
                                                            },
                                                            className: "space-y-3",
                                                            children: [
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    className: "grid grid-cols-2 gap-2",
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            children: [
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                                    className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                                    children: "Nom"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/app/login/page.tsx",
                                                                                    lineNumber: 210,
                                                                                    columnNumber: 29
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                                    type: "text",
                                                                                    required: true,
                                                                                    maxLength: 100,
                                                                                    autoComplete: "family-name",
                                                                                    placeholder: "Benali",
                                                                                    value: nom,
                                                                                    onChange: (e)=>setNom(e.target.value),
                                                                                    className: "w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/app/login/page.tsx",
                                                                                    lineNumber: 211,
                                                                                    columnNumber: 29
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 209,
                                                                            columnNumber: 27
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                            children: [
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                                    className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                                    children: "Prénom"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/app/login/page.tsx",
                                                                                    lineNumber: 223,
                                                                                    columnNumber: 29
                                                                                }, this),
                                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                                    type: "text",
                                                                                    required: true,
                                                                                    maxLength: 100,
                                                                                    autoComplete: "given-name",
                                                                                    placeholder: "Sofiane",
                                                                                    value: prenom,
                                                                                    onChange: (e)=>setPrenom(e.target.value),
                                                                                    className: "w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/app/login/page.tsx",
                                                                                    lineNumber: 224,
                                                                                    columnNumber: 29
                                                                                }, this)
                                                                            ]
                                                                        }, void 0, true, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 222,
                                                                            columnNumber: 27
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/app/login/page.tsx",
                                                                    lineNumber: 208,
                                                                    columnNumber: 25
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                            className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                            children: "Numéro de téléphone"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 238,
                                                                            columnNumber: 27
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                            type: "text",
                                                                            maxLength: 30,
                                                                            placeholder: "0598765432",
                                                                            value: telephone,
                                                                            onChange: (e)=>setTelephone(e.target.value),
                                                                            className: "w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 239,
                                                                            columnNumber: 27
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/app/login/page.tsx",
                                                                    lineNumber: 237,
                                                                    columnNumber: 25
                                                                }, this),
                                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                    children: [
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                            className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                            children: "Établissement / Hôpital"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 250,
                                                                            columnNumber: 27
                                                                        }, this),
                                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                            type: "text",
                                                                            maxLength: 150,
                                                                            placeholder: "EHS Aïn Taya",
                                                                            value: hopital,
                                                                            onChange: (e)=>setHopital(e.target.value),
                                                                            className: "w-full px-3 py-2 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                                        }, void 0, false, {
                                                                            fileName: "[project]/app/login/page.tsx",
                                                                            lineNumber: 251,
                                                                            columnNumber: 27
                                                                        }, this)
                                                                    ]
                                                                }, void 0, true, {
                                                                    fileName: "[project]/app/login/page.tsx",
                                                                    lineNumber: 249,
                                                                    columnNumber: 25
                                                                }, this)
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/app/login/page.tsx",
                                                            lineNumber: 202,
                                                            columnNumber: 23
                                                        }, this)
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 200,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                children: "Adresse Email"
                                                            }, void 0, false, {
                                                                fileName: "[project]/app/login/page.tsx",
                                                                lineNumber: 265,
                                                                columnNumber: 21
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                type: "email",
                                                                required: true,
                                                                maxLength: 255,
                                                                autoComplete: "email",
                                                                placeholder: "medecin@pancreacare.dz",
                                                                value: email,
                                                                onChange: (e)=>setEmail(e.target.value),
                                                                className: "w-full px-3.5 py-2.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                            }, void 0, false, {
                                                                fileName: "[project]/app/login/page.tsx",
                                                                lineNumber: 266,
                                                                columnNumber: 21
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 264,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                                className: "block text-[11px] font-semibold text-[#1F3D4D] mb-1",
                                                                children: "Mot de passe"
                                                            }, void 0, false, {
                                                                fileName: "[project]/app/login/page.tsx",
                                                                lineNumber: 279,
                                                                columnNumber: 21
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                type: "password",
                                                                required: true,
                                                                autoComplete: isSignUp ? "new-password" : "current-password",
                                                                placeholder: "••••••••",
                                                                value: password,
                                                                onChange: (e)=>setPassword(e.target.value),
                                                                className: "w-full px-3.5 py-2.5 rounded-xl border border-gray-200 focus:border-[#209BBF] focus:ring-2 focus:ring-[#209BBF]/20 outline-none text-xs transition-all bg-gray-50/50"
                                                            }, void 0, false, {
                                                                fileName: "[project]/app/login/page.tsx",
                                                                lineNumber: 280,
                                                                columnNumber: 21
                                                            }, this),
                                                            isSignUp && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$components$2f$PasswordRequirements$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                                                password: password,
                                                                policy: policy,
                                                                className: "mt-2"
                                                            }, void 0, false, {
                                                                fileName: "[project]/app/login/page.tsx",
                                                                lineNumber: 290,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 278,
                                                        columnNumber: 19
                                                    }, this),
                                                    !isSignUp && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "text-right pt-0.5",
                                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                                            href: "/forgot-password",
                                                            className: "text-[11px] text-[#209BBF] hover:underline font-medium",
                                                            children: "Mot de passe oublié ?"
                                                        }, void 0, false, {
                                                            fileName: "[project]/app/login/page.tsx",
                                                            lineNumber: 296,
                                                            columnNumber: 23
                                                        }, this)
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 295,
                                                        columnNumber: 21
                                                    }, this),
                                                    error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-[11px] text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2",
                                                        children: error
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 303,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                        type: "submit",
                                                        disabled: isLoading || isSignUp && password.length > 0 && !passwordCompliant,
                                                        className: "w-full py-2.5 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-300 mt-2 text-xs disabled:opacity-60 disabled:cursor-not-allowed",
                                                        children: isLoading ? "Veuillez patienter..." : isSignUp ? "Envoyer ma demande" : "Se connecter"
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/login/page.tsx",
                                                        lineNumber: 308,
                                                        columnNumber: 19
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/app/login/page.tsx",
                                                lineNumber: 198,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/app/login/page.tsx",
                                        lineNumber: 170,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/app/login/page.tsx",
                                    lineNumber: 169,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "shrink-0 border-t border-gray-100 p-6 sm:p-8 md:p-10 pt-3 md:pt-4",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "max-w-md mx-auto w-full text-center text-xs text-gray-600",
                                        children: [
                                            isSignUp ? "Déjà un compte ?" : "Pas encore de compte ?",
                                            " ",
                                            " ",
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                type: "button",
                                                onClick: ()=>setIsSignUp(!isSignUp),
                                                className: "text-[#1D7893] font-bold underline ml-1 cursor-pointer",
                                                children: isSignUp ? "Se connecter" : "S'inscrire"
                                            }, void 0, false, {
                                                fileName: "[project]/app/login/page.tsx",
                                                lineNumber: 322,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/app/login/page.tsx",
                                        lineNumber: 320,
                                        columnNumber: 17
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/app/login/page.tsx",
                                    lineNumber: 319,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, isSignUp ? "signup-form" : "login-form", true, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 160,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
                            layout: true,
                            transition: {
                                duration: 0.6,
                                ease: "easeInOut"
                            },
                            className: `hidden md:block w-1/2 min-h-[600px] relative overflow-hidden ${isSignUp ? "md:order-1" : "md:order-2"}`,
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                    src: __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$about$2d$doctors$2e$png$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$assets$2f$about$2d$doctors$2e$png__$28$static__in__ecmascript$2c$__tag__client$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object__with__data__url$2c$__ecmascript$29$__["default"],
                                    alt: "Équipe médicale spécialiste du pancréas",
                                    fill: true,
                                    priority: true,
                                    className: "object-cover"
                                }, void 0, false, {
                                    fileName: "[project]/app/login/page.tsx",
                                    lineNumber: 341,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "absolute inset-0 bg-gradient-to-t from-[#1D7893]/90 via-[#1D7893]/40 to-transparent flex flex-col justify-end p-8 text-white",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                            className: "text-xl font-bold mb-2",
                                            children: showSignUpPitch ? "Rejoignez la plateforme" : "Bienvenue Docteur"
                                        }, void 0, false, {
                                            fileName: "[project]/app/login/page.tsx",
                                            lineNumber: 350,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-xs text-cyan-100 mb-6 leading-relaxed font-light max-w-sm",
                                            children: showSignUpPitch ? "Demandez votre accès : un administrateur vérifie chaque inscription avant de l'activer." : "Accédez instantanément aux dossiers patients, à l'historique et aux recommandations thérapeutiques."
                                        }, void 0, false, {
                                            fileName: "[project]/app/login/page.tsx",
                                            lineNumber: 353,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>setIsSignUp(!isSignUp),
                                            className: "w-fit px-5 py-2 border border-white/80 rounded-full text-xs font-semibold backdrop-blur-sm hover:bg-white hover:text-[#1D7893] transition-all duration-300 shadow-sm",
                                            children: isSignUp ? "Déjà inscrit ? Se connecter" : "Pas de compte ? S'inscrire"
                                        }, void 0, false, {
                                            fileName: "[project]/app/login/page.tsx",
                                            lineNumber: 359,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/app/login/page.tsx",
                                    lineNumber: 349,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 334,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 155,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/login/page.tsx",
            lineNumber: 123,
            columnNumber: 9
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/login/page.tsx",
        lineNumber: 121,
        columnNumber: 5
    }, this);
}
_s(AuthPageContent, "cu2vSEzaZVyrUwrn7ufwSIhcOGs=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useSearchParams"],
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"]
    ];
});
_c = AuthPageContent;
/**
 * Écran affiché après une inscription.
 *
 * Le compte est en attente de validation : le message dit explicitement que la
 * connexion n'est pas encore possible et pourquoi. Sans cela, le médecin
 * reviendrait sur /login, échouerait, et croirait que la plateforme est
 * cassée au lieu d'être simplement en attente.
 */ function ValidationPending({ email, message, onBack }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "min-h-screen w-full bg-[#EAF4F7] flex items-center justify-center p-4 sm:p-6 font-serif",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cyan-50 text-center",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                        className: "w-8 h-8",
                        fill: "none",
                        viewBox: "0 0 24 24",
                        stroke: "currentColor",
                        strokeWidth: "2",
                        "aria-hidden": "true",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                            strokeLinecap: "round",
                            strokeLinejoin: "round",
                            d: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        }, void 0, false, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 397,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/login/page.tsx",
                        lineNumber: 396,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 395,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-xl font-extrabold text-[#1D7893] mb-2",
                    children: "Demande transmise"
                }, void 0, false, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 401,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: "text-xs text-gray-600 mb-4 leading-relaxed",
                    children: message
                }, void 0, false, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 402,
                    columnNumber: 9
                }, this),
                email && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: "text-xs text-gray-600 mb-6",
                    children: [
                        "Adresse déclarée :",
                        " ",
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "font-semibold text-[#1F3D4D]",
                            children: email
                        }, void 0, false, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 407,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 405,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-3.5 bg-blue-50/80 rounded-xl border border-blue-100 text-[11px] text-[#1F3D4D] mb-6 text-left",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                            children: "En cas d'oubli de mot de passe :"
                        }, void 0, false, {
                            fileName: "[project]/app/login/page.tsx",
                            lineNumber: 412,
                            columnNumber: 11
                        }, this),
                        " la plateforme n'envoie aucun email. Passez par « Mot de passe oublié » : votre demande est transmise à l'administration, qui vous communiquera un lien de réinitialisation à usage unique."
                    ]
                }, void 0, true, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 411,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                    onClick: onBack,
                    className: "w-full py-3 bg-[#1D7893] hover:bg-[#209BBF] text-white font-semibold rounded-xl shadow-md transition-all duration-200 text-sm",
                    children: "Retour à la connexion"
                }, void 0, false, {
                    fileName: "[project]/app/login/page.tsx",
                    lineNumber: 418,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/login/page.tsx",
            lineNumber: 394,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/login/page.tsx",
        lineNumber: 393,
        columnNumber: 5
    }, this);
}
_c1 = ValidationPending;
function AuthPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Suspense"], {
        fallback: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "min-h-screen bg-[#EAF4F7]"
        }, void 0, false, {
            fileName: "[project]/app/login/page.tsx",
            lineNumber: 430,
            columnNumber: 30
        }, this),
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthPageContent, {}, void 0, false, {
            fileName: "[project]/app/login/page.tsx",
            lineNumber: 430,
            columnNumber: 77
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/login/page.tsx",
        lineNumber: 430,
        columnNumber: 10
    }, this);
}
_c2 = AuthPage;
var _c, _c1, _c2;
__turbopack_context__.k.register(_c, "AuthPageContent");
__turbopack_context__.k.register(_c1, "ValidationPending");
__turbopack_context__.k.register(_c2, "AuthPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/assets/about-doctors.png (static in ecmascript, tag client)", ((__turbopack_context__) => {

__turbopack_context__.q("/_next/static/media/about-doctors.0d7d7ezxf3dpj.png");}),
"[project]/assets/about-doctors.png.mjs { IMAGE => \"[project]/assets/about-doctors.png (static in ecmascript, tag client)\" } [app-client] (structured image object with data url, ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$about$2d$doctors$2e$png__$28$static__in__ecmascript$2c$__tag__client$29$__ = __turbopack_context__.i("[project]/assets/about-doctors.png (static in ecmascript, tag client)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$about$2d$doctors$2e$png__$28$static__in__ecmascript$2c$__tag__client$29$__["default"],
    width: 612,
    height: 614,
    blurWidth: 8,
    blurHeight: 8,
    blurDataURL: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAA/UlEQVR42h2NT0vCcABAf5+rawSdPHWpQ+cgjEr8k0GEhWullWFO11DTyDpYYGaSRlK6SurSnGOMEYX1NV6r63sPnliKJwhup/CvbRCISURTWUKJNMvSLguxLcSfjO4pRPxzlORVZLWInM0Ty2gEPCcWg6H/YHMnyU3jCjlXQFXS5MqnRDwupP0DJCVPMp2l3mhyUq1RKReoXNaIqyXEfDjMdeuenv7MYDDENC0sw0TJ5NDKZ4ip4AqPTy/YQ5PR9w/Wu8Fdq8Pk+ASadoyYnp3x3g36eg/HcXHdD9oXVYrSOs3bDmLM5+NQPaLb1bFth6/PEf3OA8brG+f1Nr/McLhT0v0BOwAAAABJRU5ErkJggg=="
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/assets/logo.png (static in ecmascript, tag client)", ((__turbopack_context__) => {

__turbopack_context__.q("/_next/static/media/logo.2knwgnm2ys_29.png");}),
"[project]/assets/logo.png.mjs { IMAGE => \"[project]/assets/logo.png (static in ecmascript, tag client)\" } [app-client] (structured image object with data url, ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$logo$2e$png__$28$static__in__ecmascript$2c$__tag__client$29$__ = __turbopack_context__.i("[project]/assets/logo.png (static in ecmascript, tag client)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$assets$2f$logo$2e$png__$28$static__in__ecmascript$2c$__tag__client$29$__["default"],
    width: 120,
    height: 69,
    blurWidth: 8,
    blurHeight: 5,
    blurDataURL: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAFCAYAAAB4ka1VAAAAmUlEQVR42jWJuw6CMBRA+7jthdhabKogkiCV+GDRxBAHxFnRlcTFzf//BmHwbOccQgEV13Mf5LsDj+KcTxcFmKQcWkFFaAibzDKR7Fvbdn3gTzf0lx7X5yeWzRvibUMIZZyCkOiWKShjQEVWaOuYDBXhEskI6Mjqqq5N8+jmr8/XXe8dE1KQP4NI6dIUV74MfXUMMr+hHPj4fpInDaK0sLD1AAAAAElFTkSuQmCC"
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/components/PasswordRequirements.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>PasswordRequirements,
    "isPasswordCompliant",
    ()=>isPasswordCompliant
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/lib/api.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
function buildRules(password, policy) {
    const rules = [
        {
            id: "min_length",
            label: `Au moins ${policy.min_length} caractères`,
            satisfied: password.length >= policy.min_length
        }
    ];
    if (policy.require_lowercase) {
        rules.push({
            id: "lowercase",
            label: "Une lettre minuscule (a-z)",
            satisfied: /[a-z]/.test(password)
        });
    }
    if (policy.require_uppercase) {
        rules.push({
            id: "uppercase",
            label: "Une lettre majuscule (A-Z)",
            satisfied: /[A-Z]/.test(password)
        });
    }
    if (policy.require_digit) {
        rules.push({
            id: "digit",
            label: "Un chiffre (0-9)",
            satisfied: /[0-9]/.test(password)
        });
    }
    return rules;
}
function isPasswordCompliant(password, policy) {
    return buildRules(password, policy).every((rule)=>rule.satisfied);
}
function PasswordRequirements({ password, policy, className = "" }) {
    _s();
    const [fetchedPolicy, setFetchedPolicy] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "PasswordRequirements.useEffect": ()=>{
            if (policy) return;
            let active = true;
            (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["getPasswordPolicy"])().then({
                "PasswordRequirements.useEffect": (p)=>{
                    if (active) setFetchedPolicy(p);
                }
            }["PasswordRequirements.useEffect"]);
            return ({
                "PasswordRequirements.useEffect": ()=>{
                    active = false;
                }
            })["PasswordRequirements.useEffect"];
        }
    }["PasswordRequirements.useEffect"], [
        policy
    ]);
    const resolved = policy ?? fetchedPolicy ?? __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["DEFAULT_PASSWORD_POLICY"];
    const rules = buildRules(password, resolved);
    const remaining = rules.filter((rule)=>!rule.satisfied).length;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: `rounded-xl border border-gray-100 bg-gray-50/60 px-3 py-2.5 ${className}`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-[11px] font-semibold text-[#1F3D4D] mb-1.5",
                children: password.length === 0 ? "Exigences du mot de passe" : remaining === 0 ? "Mot de passe conforme" : `Il manque ${remaining} exigence${remaining > 1 ? "s" : ""}`
            }, void 0, false, {
                fileName: "[project]/components/PasswordRequirements.tsx",
                lineNumber: 76,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                className: "space-y-1",
                children: rules.map((rule)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                        className: `flex items-center gap-1.5 text-[11px] transition-colors ${rule.satisfied ? "text-emerald-700" : "text-gray-500"}`,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                "aria-hidden": "true",
                                className: `flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full text-[9px] font-bold ${rule.satisfied ? "bg-emerald-100 text-emerald-700" : "bg-gray-200 text-gray-400"}`,
                                children: rule.satisfied ? "✓" : "•"
                            }, void 0, false, {
                                fileName: "[project]/components/PasswordRequirements.tsx",
                                lineNumber: 91,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: rule.satisfied ? "line-through opacity-70" : "",
                                children: rule.label
                            }, void 0, false, {
                                fileName: "[project]/components/PasswordRequirements.tsx",
                                lineNumber: 99,
                                columnNumber: 13
                            }, this)
                        ]
                    }, rule.id, true, {
                        fileName: "[project]/components/PasswordRequirements.tsx",
                        lineNumber: 85,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/components/PasswordRequirements.tsx",
                lineNumber: 83,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/components/PasswordRequirements.tsx",
        lineNumber: 75,
        columnNumber: 5
    }, this);
}
_s(PasswordRequirements, "CQiNB+imglKnHeztv29gIh8PCvs=");
_c = PasswordRequirements;
var _c;
__turbopack_context__.k.register(_c, "PasswordRequirements");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/lib/api.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DEFAULT_PASSWORD_POLICY",
    ()=>DEFAULT_PASSWORD_POLICY,
    "TOKEN_KEY",
    ()=>TOKEN_KEY,
    "accepterCompte",
    ()=>accepterCompte,
    "bloquerCompte",
    ()=>bloquerCompte,
    "changePassword",
    ()=>changePassword,
    "clearToken",
    ()=>clearToken,
    "cloturerDemandeReinitialisation",
    ()=>cloturerDemandeReinitialisation,
    "createEvaluationAndCalculate",
    ()=>createEvaluationAndCalculate,
    "createPatientAndCalculate",
    ()=>createPatientAndCalculate,
    "debloquerCompte",
    ()=>debloquerCompte,
    "definirMotDePasseTemporaire",
    ()=>definirMotDePasseTemporaire,
    "forgotPassword",
    ()=>forgotPassword,
    "genererLienReinitialisation",
    ()=>genererLienReinitialisation,
    "getAdminComptes",
    ()=>getAdminComptes,
    "getAdminStatistiques",
    ()=>getAdminStatistiques,
    "getCurrentSession",
    ()=>getCurrentSession,
    "getDemandesReinitialisation",
    ()=>getDemandesReinitialisation,
    "getDossierDetail",
    ()=>getDossierDetail,
    "getPasswordPolicy",
    ()=>getPasswordPolicy,
    "getPatient",
    ()=>getPatient,
    "getPatientDetail",
    ()=>getPatientDetail,
    "getPatientEvaluations",
    ()=>getPatientEvaluations,
    "getPatients",
    ()=>getPatients,
    "getRecommendations",
    ()=>getRecommendations,
    "login",
    ()=>login,
    "resetPassword",
    ()=>resetPassword,
    "signup",
    ()=>signup,
    "updatePatient",
    ()=>updatePatient
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
const API_URL = ("TURBOPACK compile-time value", "http://127.0.0.1:8000") ?? "http://127.0.0.1:8000";
const TOKEN_KEY = "token";
const clearToken = ()=>{
    if ("TURBOPACK compile-time truthy", 1) localStorage.removeItem(TOKEN_KEY);
};
async function request(path, body, method = body ? "POST" : "GET") {
    const token = ("TURBOPACK compile-time truthy", 1) ? localStorage.getItem(TOKEN_KEY) : "TURBOPACK unreachable";
    let res;
    try {
        res = await fetch(`${API_URL}${path}`, {
            method,
            headers: {
                "Content-Type": "application/json",
                ...token ? {
                    Authorization: `Bearer ${token}`
                } : {}
            },
            body: body ? JSON.stringify(body) : undefined
        });
    } catch (cause) {
        const reason = cause instanceof Error ? ` (${cause.message})` : "";
        throw new Error(`Impossible de joindre le serveur [${method} ${path}].${reason}`);
    }
    const data = await res.json().catch(()=>({}));
    if (!res.ok) throw new Error(data.detail ?? "Une erreur est survenue.");
    return data;
}
const login = (email, password)=>request("/auth/login", {
        email,
        password
    });
const signup = (payload)=>request("/auth/signup", payload);
const forgotPassword = (email)=>request("/auth/forgot-password", {
        email
    });
const resetPassword = (jeton, nouveauMotDePasse)=>request("/auth/reset-password", {
        jeton,
        nouveau_mot_de_passe: nouveauMotDePasse
    });
const changePassword = (ancienMotDePasse, nouveauMotDePasse)=>request("/auth/change-password", {
        ancien_mot_de_passe: ancienMotDePasse,
        nouveau_mot_de_passe: nouveauMotDePasse
    });
const getCurrentSession = ()=>request("/auth/me", undefined, "GET");
const DEFAULT_PASSWORD_POLICY = {
    min_length: 8,
    require_lowercase: true,
    require_uppercase: true,
    require_digit: true
};
const getPasswordPolicy = ()=>request("/auth/password-policy", undefined, "GET").catch(()=>DEFAULT_PASSWORD_POLICY);
const getAdminStatistiques = ()=>request("/admin/statistiques", undefined, "GET");
const getAdminComptes = (options = {})=>{
    const params = new URLSearchParams();
    if (options.statut) params.set("statut", options.statut);
    if (options.recherche) params.set("recherche", options.recherche);
    const suffixe = params.toString();
    return request(`/admin/comptes${suffixe ? `?${suffixe}` : ""}`, undefined, "GET");
};
const accepterCompte = (idCompte)=>request(`/admin/comptes/${idCompte}/accepter`, {});
const bloquerCompte = (idCompte, motif)=>request(`/admin/comptes/${idCompte}/bloquer`, {
        motif: motif || null
    });
const debloquerCompte = (idCompte)=>request(`/admin/comptes/${idCompte}/debloquer`, {});
const definirMotDePasseTemporaire = (idCompte, nouveauMotDePasse)=>request(`/admin/comptes/${idCompte}/mot-de-passe-temporaire`, {
        nouveau_mot_de_passe: nouveauMotDePasse
    });
const getDemandesReinitialisation = (statut = "en_attente")=>request(`/admin/demandes-reinitialisation?statut=${encodeURIComponent(statut)}`, undefined, "GET");
const genererLienReinitialisation = (idDemande)=>request(`/admin/demandes-reinitialisation/${idDemande}/lien`, {});
const cloturerDemandeReinitialisation = (idDemande, statut)=>request(`/admin/demandes-reinitialisation/${idDemande}/cloturer?statut=${statut}`, {});
const getPatients = (nom)=>request(`/patients${nom ? `?nom=${encodeURIComponent(nom)}` : ""}`, undefined, "GET");
const getPatient = (idPatient)=>request(`/patients/${idPatient}`, undefined, "GET");
const updatePatient = (idPatient, payload)=>request(`/patients/${idPatient}`, payload, "PUT");
const getPatientDetail = (idPatient)=>request(`/patients/${idPatient}/detail`, undefined, "GET");
const getDossierDetail = (idDossier)=>request(`/dossiers/full/${idDossier}`, undefined, "GET");
// --- Mapping formulaire (camelCase FR) -> enums backend (snake_case) ---------
const ENUM_MAP = {
    etatNutritionnel: {
        "dénutrition modérée": "denutrition_moderee",
        "dénutrition sévère": "denutrition_severe"
    },
    diabete: {
        "récent (<2 ans)": "recent_moins_2ans"
    },
    statutDpd: {
        "déficit partiel": "deficit_partiel",
        "déficit complet": "deficit_complet"
    },
    localisationTumorale: {
        "tête/crochet": "tete_crochet",
        "corps-queue": "corps_queue"
    },
    contactAms: {
        "pas de contact": "absent",
        "<180°": "lt180",
        "≥180°": "ge180"
    },
    contactTroncCoeliaque: {
        "pas de contact": "absent",
        "<180°": "lt180",
        "≥180°": "ge180"
    },
    contactAhc: {
        "pas de contact": "absent",
        "court reconstructible": "court_sans_envahissement",
        "non reconstructible": "envahissant"
    },
    contactVmsVp: {
        "<180° sans irrégularité": "lt180_sans_irregularite",
        "≥180° ou irrégularité ou occlusion reconstructible": "ge180_ou_irregularite",
        "occlusion non reconstructible": "occlusion_non_reconstructible"
    },
    statutBrca: {
        "non testé": "non_teste",
        "muté": "mute",
        "non muté": "non_mute"
    },
    statutKras: {
        "non testé": "non_teste",
        "G12C": "g12c",
        "G12D": "g12d",
        "G12V": "g12v",
        "autre": "autre_mute"
    },
    statutMsiDmmr: {
        "non testé": "non_teste",
        "positif": "msi_h",
        "négatif": "mss"
    },
    fusionNtrk: {
        "non testé": "non_teste",
        "oui": "positif",
        "non": "negatif"
    },
    fusionNrg1: {
        "non testé": "non_teste",
        "oui": "positif",
        "non": "negatif"
    }
};
const toEnum = (value, key)=>{
    if (value == null || value === "") return null;
    if (key === "statutDpd" && value === "normal") return "normal";
    return ENUM_MAP[key]?.[value] ?? value;
};
const toNumber = (value)=>{
    if (value == null || value === "") return null;
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
};
function buildEvaluationPayload(data) {
    const today = new Date().toISOString().slice(0, 10);
    const bilirubine = toNumber(data.bilirubine);
    const lsnBilirubine = toNumber(data.lsnBilirubine);
    const bilirubine_ratio_lsn = bilirubine != null && lsnBilirubine && lsnBilirubine > 0 ? bilirubine / lsnBilirubine : null;
    const metastases_presentes = Boolean(data.metastases);
    const duree = toNumber(data.dureeChimiotherapieMois);
    const dateDebutCourante = duree != null ? new Date(Date.now() - duree * 30.4375 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10) : null;
    const reponseTraitementPrecedent = data.reponseTraitementPrecedent || data.reponseTraitementEnCours || null;
    const currentLine = Number(data.ligneTraitementActuelle || 1);
    const received = Array.isArray(data.traitementsRecus) ? data.traitementsRecus.filter(Boolean) : [];
    if (currentLine >= 2 && received.length === 0) {
        throw new Error("Le traitement précédent est obligatoire à partir de la deuxième ligne.");
    }
    if (currentLine >= 2 && !reponseTraitementPrecedent) {
        throw new Error("La réponse au traitement précédent est obligatoire à partir de la deuxième ligne.");
    }
    if (duree == null) {
        throw new Error("La durée de la chimiothérapie doit être renseignée.");
    }
    const previousTreatments = received.map((name, index)=>({
            numero_ligne: Math.max(1, currentLine - received.length + index),
            date_debut: null,
            date_fin: null,
            reponse: index === received.length - 1 ? reponseTraitementPrecedent : null,
            toxicite_residuelle: false,
            type_toxicite: null,
            termine_comme_prevu: null,
            notes: name
        }));
    const traitements = [
        ...previousTreatments,
        {
            numero_ligne: currentLine,
            date_debut: dateDebutCourante,
            date_fin: null,
            reponse: null,
            toxicite_residuelle: Boolean(data.toxiciteResiduelle),
            type_toxicite: data.detailsToxicite || null,
            termine_comme_prevu: null,
            notes: null
        }
    ];
    return {
        date_evaluation: today,
        contexte: "diagnostic",
        ecog: data.ecog ?? null,
        etat_nutritionnel: toEnum(data.etatNutritionnel, "etatNutritionnel") ?? "inconnu",
        douleur_presente: data.douleur === "présente" ? true : data.douleur === "absente" ? false : null,
        intensite_douleur: data.intensiteDouleur ? toNumber(data.intensiteDouleur) ?? null : null,
        ictere: Boolean(data.ictere),
        diabete: toEnum(data.diabete, "diabete") ?? "inconnu",
        biologie: {
            ca19_9: toNumber(data.ca199),
            cholestase: Boolean(data.cholestase),
            bilirubine,
            bilirubine_ratio_lsn,
            statut_dpd: toEnum(data.statutDpd, "statutDpd") ?? "non_teste",
            albuminemie: toNumber(data.albuminemie)
        },
        imageries: [
            {
                type_imagerie: "TDM",
                date_imagerie: today,
                localisation_tumorale: toEnum(data.localisationTumorale, "localisationTumorale") ?? "inconnu",
                taille_tumorale_cm: toNumber(data.tailleTumorale),
                contact_ams: toEnum(data.contactAms, "contactAms"),
                contact_tronc_coeliaque: toEnum(data.contactTroncCoeliaque, "contactTroncCoeliaque"),
                contact_art_hepatique: toEnum(data.contactAhc, "contactAhc"),
                contact_vms_vp: toEnum(data.contactVmsVp, "contactVmsVp"),
                extension_ganglionnaire_regionale: Boolean(data.adenopathieRegionale),
                extension_ganglionnaire_distance: Boolean(data.adenopathieDistance),
                metastases_presentes,
                metastases: metastases_presentes ? data.sitesMetastases?.length ? data.sitesMetastases.map((site)=>({
                        site,
                        detail: null
                    })) : [
                    {
                        site: "autre",
                        detail: null
                    }
                ] : []
            }
        ],
        histologie: {
            preuve_histologique: Boolean(data.preuveHistologique),
            statut_brca_germinal: toEnum(data.statutBrca, "statutBrca") ?? "non_teste",
            statut_kras: toEnum(data.statutKras, "statutKras") ?? "non_teste",
            statut_msi_dmmr: toEnum(data.statutMsiDmmr, "statutMsiDmmr") ?? "non_teste",
            fusion_ntrk: toEnum(data.fusionNtrk, "fusionNtrk") ?? "non_teste",
            fusion_nrg1: toEnum(data.fusionNrg1, "fusionNrg1") ?? "non_teste"
        },
        analyses: [],
        comorbidites: [],
        parcours: {
            angiocholite: data.angiocholite ?? null,
            comorbidites_lourdes: data.comorbiditesLourdes ?? null,
            tumeur_controlee: data.tumeurControle ?? null,
            nouvelles_metastases: data.nouvellesMetastases ?? null,
            chirurgie_d_emblee: data.chirurgieDembleePrevue ?? null,
            traitement_medical_prevu: data.traitementMedicalPrevu ?? null,
            pas_de_progression_apres_16_semaines_platine: data.pasDeProgressionApres16SemainesPlatine ?? null,
            date_reevaluation: today,
            commentaire: null
        },
        traitements
    };
}
function buildFullPatientPayload(data) {
    return {
        nom: data.nom,
        prenom: data.prenom,
        date_naissance: data.dateNaissance || null,
        sexe: data.sexe || null,
        telephone: data.telephone || null,
        adresse: data.adresse || null,
        antecedents: [],
        mutations: [],
        evaluation: buildEvaluationPayload(data)
    };
}
const createPatientAndCalculate = async (formData)=>{
    const created = await request("/patients/full", buildFullPatientPayload(formData));
    const calculated = await request(`/clinical-rules/evaluations/${created.id_evaluation}/calculate`, {
        categorie_t: formData.categorieT,
        categorie_n: formData.categorieN,
        categorie_m: formData.categorieM,
        version_moteur: "tncd-2024-v1"
    });
    return {
        created,
        calculated
    };
};
const createEvaluationAndCalculate = async (idPatient, formData)=>{
    const created = await request(`/patients/${idPatient}/evaluations`, buildEvaluationPayload(formData));
    const calculated = await request(`/clinical-rules/evaluations/${created.id_evaluation}/calculate`, {
        categorie_t: formData.categorieT,
        categorie_n: formData.categorieN,
        categorie_m: formData.categorieM,
        version_moteur: "tncd-2024-v1"
    });
    return {
        created,
        calculated
    };
};
const getRecommendations = (idEvaluation)=>request(`/clinical-rules/evaluations/${idEvaluation}/recommendations`, undefined, "GET");
const getPatientEvaluations = (idPatient)=>request(`/patients/${idPatient}/evaluations`, undefined, "GET");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=_08w1etr._.js.map