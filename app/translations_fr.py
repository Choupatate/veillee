"""French interface strings (FEATURES.md F38).

Keys are the English source strings exactly as they appear in the
templates, so a missing entry falls back to readable English rather than a
raw key. `tests/test_i18n.py` walks the templates and fails if any string
passed to `_()` is missing here, so the fallback stays a safety net rather
than a habit.

Tone note: the app addresses the child directly in a few places ("before
you were born"), and French keeps that familiar register — "tu", never
"vous". The family writing the book is being spoken to, not a customer.
"""

TRANSLATIONS_FR = {
    # --- the app's own name (STORYBOOK_TITLE overrides this in either
    # language; this is only the default when no family title is set) -----
    "Storybook": "La Veillée",

    # --- navigation and chrome ---------------------------------------------
    "Skip to content": "Aller au contenu",
    "Switch light and dark. Hold, or press the down arrow, for theme "
    "options.":
        "Basculer clair / sombre. Maintenez appuyé, ou appuyez sur la "
        "flèche du bas, pour les options d'apparence.",
    "Hold for theme options": "Maintenez pour les options d'apparence",
    "Colour scheme": "Palette",
    "How it looks": "L'apparence",
    "Light and dark": "Clair et sombre",
    "The half-moon button in the nav switches between them. Hold it down "
    "for the full set — including going back to whatever your phone or "
    "computer does on its own.":
        "Le bouton demi-lune de la barre de navigation bascule de l'un à "
        "l'autre. Maintenez-le appuyé pour tout le choix — y compris le "
        "retour au réglage de votre téléphone ou de votre ordinateur.",
    "Under that same hold: the book's whole look, pictures and all. It "
    "changes your screen only, not anyone else's.":
        "Sous ce même appui long : toute l'apparence du livre, images "
        "comprises. Cela ne change que votre écran, pas celui des autres.",
    "The flame button turns the slow flicker on the page on and off. It is "
    "off for good once you turn it off, on this screen.":
        "Le bouton flamme active ou désactive le lent vacillement de la "
        "page. Une fois désactivé, il le reste sur cet écran.",
    "Dark": "Sombre",
    "Light": "Clair",
    "Manuscript": "Manuscrit",
    "System": "Système",
    "Theme": "Thème",
    "Firelight": "Lueur du feu",
    "Language": "Langue",
    "People": "Personnes",
    "Help": "Aide",
    "Accounts": "Comptes",
    "Account": "Compte",
    "+ New story": "+ Nouvelle histoire",
    "+ Instant": "+ Instant",
    "Log out": "Se déconnecter",
    "Timeline": "Fil du temps",
    "Edit": "Modifier",
    "Save": "Enregistrer",
    "Cancel": "Annuler",
    "Delete": "Supprimer",
    "Restore": "Restaurer",
    "Import": "Importer",

    # --- login / accounts ---------------------------------------------------
    "Log in": "Se connecter",
    "A private memory journal.": "Un journal de souvenirs, rien qu'à vous.",
    "Username": "Nom d'utilisateur",
    "Password": "Mot de passe",
    "Incorrect password.": "Mot de passe incorrect.",
    "Incorrect username or password.": "Nom d'utilisateur ou mot de passe incorrect.",
    "Incorrect invite code.": "Code d'invitation incorrect.",
    "Don't have an account?": "Pas encore de compte ?",
    "Request one.": "En demander un.",
    "No accounts yet —": "Aucun compte pour l'instant —",
    "request the first one": "demandez le premier",
    "to get started.": "pour commencer.",
    "Request an account": "Demander un compte",
    "Request account": "Demander un compte",
    "Ask whoever set this up for the invite code.":
        "Demandez le code d'invitation à la personne qui a installé ce livre.",
    "Your name": "Votre nom",
    "Note (optional)": "Note (facultatif)",
    "e.g. Milo's godmother": "ex. la marraine de Milo",
    "Invite code": "Code d'invitation",
    "Back to log in": "Retour à la connexion",
    "You're the first account on this book — it's been created as admin.":
        "Vous êtes le premier compte de ce livre — il a été créé en tant "
        "qu'administrateur.",
    "Thanks — an admin will review your request soon.":
        "Merci — un administrateur examinera votre demande bientôt.",

    # --- invitations and open requests (F39) --------------------------------
    "Ask to join, and someone in the family will let you in.":
        "Demandez à nous rejoindre, et quelqu'un de la famille vous ouvrira.",
    "Invite code (optional)": "Code d'invitation (facultatif)",
    "Leave this empty if you weren't given one — an admin will review your "
    "request.":
        "Laissez vide si on ne vous en a pas donné — un administrateur "
        "examinera votre demande.",
    "There are too many requests waiting to be reviewed. Try again later.":
        "Trop de demandes attendent d'être examinées. Réessayez plus tard.",
    "+ Invite": "+ Inviter",
    "Invite someone": "Inviter quelqu'un",
    "Pick who this is for and send them the link. They choose their own "
    "username and password — you never have to handle either.":
        "Choisissez pour qui, puis envoyez-lui le lien. Elle choisira "
        "elle-même son nom d'utilisateur et son mot de passe — vous n'avez "
        "jamais à les manipuler.",
    "Expires after (days)": "Expire après (jours)",
    "Create invitation": "Créer l'invitation",
    "Invitations sent": "Invitations envoyées",
    "Withdraw": "Retirer",
    "expires {date}": "expire le {date}",
    "Choose your login": "Choisissez vos identifiants",
    "You've been invited as {name}. Choose a username and a password — "
    "nobody else will see them.":
        "Vous avez été invité·e en tant que {name}. Choisissez un nom "
        "d'utilisateur et un mot de passe — personne d'autre ne les verra.",
    "3-32 characters: lowercase letters, numbers, hyphens.":
        "3 à 32 caractères : minuscules, chiffres, tirets.",
    "Confirm password": "Confirmer le mot de passe",
    "Create my account": "Créer mon compte",
    "Your account is ready — log in with it below.":
        "Votre compte est prêt — connectez-vous avec ci-dessous.",
    "Invitation not valid": "Invitation non valable",
    "This invitation isn't valid anymore — it may have already been used, "
    "withdrawn, or expired. Ask whoever sent it to you for a new one.":
        "Cette invitation n'est plus valable — elle a peut-être déjà été "
        "utilisée, retirée, ou elle a expiré. Demandez-en une nouvelle à la "
        "personne qui vous l'a envoyée.",
    "{name} already has an account": "{name} a déjà un compte",
    "already in the book: {name}": "déjà dans le livre : {name}",
    "{name} is already in the book and can already log in — approving this "
    "would give the same person a second account.":
        "{name} est déjà dans le livre et peut déjà se connecter — approuver "
        "cette demande donnerait un deuxième compte à la même personne.",
    "{name} is already in the book. Bind this request to them rather than "
    "adding a second entry.":
        "{name} est déjà dans le livre. Rattachez cette demande à cette "
        "personne plutôt que d'en ajouter une deuxième.",

    # --- audience groups (F40) ----------------------------------------------
    "Groups": "Cercles",
    "New group": "Nouveau cercle",
    "Create group": "Créer le cercle",
    "Save group": "Enregistrer le cercle",
    "No groups yet.": "Aucun cercle pour l'instant.",
    "e.g. Just us": "ex. Rien que nous",
    "nobody yet": "personne pour l'instant",
    "Who's in it": "Qui en fait partie",
    "can't log in yet": "ne peut pas encore se connecter",
    "A group is a handful of people a story can be kept to. Stories with no "
    "group are for everyone — that stays the default.":
        "Un cercle, c'est une poignée de personnes à qui une histoire peut "
        "être réservée. Les histoires sans cercle sont pour tout le monde — "
        "et ça reste le cas par défaut.",
    "Taking someone out means they stop seeing those stories straight away.":
        "Retirer quelqu'un lui retire l'accès à ces histoires "
        "immédiatement.",
    "{n} story": "{n} histoire",
    "{n} stories": "{n} histoires",
    "{n} story is kept to this group.": "{n} histoire est réservée à ce cercle.",
    "{n} stories are kept to this group.":
        "{n} histoires sont réservées à ce cercle.",

    # --- groups anyone can make (F41) ---------------------------------------
    "View": "Voir",
    "made by {name}": "créé par {name}",
    "{name} made this one.": "C'est {name} qui l'a créé.",
    "Anyone can make one, and the people in a group are the ones who can "
    "change it.":
        "Tout le monde peut en créer un, et ce sont les personnes qui en font "
        "partie qui peuvent le modifier.",
    "Name it first, then pick who's in it on the next screen. You'll be in it "
    "yourself.":
        "Donnez-lui d'abord un nom, puis choisissez qui en fait partie à "
        "l'écran suivant. Vous en ferez partie vous-même.",
    "A group is changed by the people in it, or by an admin.":
        "Un cercle se modifie par les personnes qui en font partie, ou par "
        "un administrateur.",
    "A group is changed by the people in it, so if you take yourself out you "
    "won't be able to change it again.":
        "Un cercle se modifie par les personnes qui en font partie : si vous "
        "vous retirez, vous ne pourrez plus le modifier.",
    "{n} of them was written by someone else. Adding a person here opens "
    "their writing too, not only yours.":
        "{n} d'entre elles a été écrite par quelqu'un d'autre. Ajouter une "
        "personne ici ouvre aussi ses écrits, pas seulement les vôtres.",
    "{n} of them were written by someone else. Adding a person here opens "
    "their writing too, not only yours.":
        "{n} d'entre elles ont été écrites par quelqu'un d'autre. Ajouter une "
        "personne ici ouvre aussi ses écrits, pas seulement les vôtres.",
    "This book is holding as many groups as it keeps. Rename or reuse one "
    "instead of adding another.":
        "Ce livre contient déjà autant de cercles qu'il en garde. Renommez ou "
        "réutilisez-en un plutôt que d'en ajouter un autre.",
    # Flash messages raised as groups.GroupError — the template stays the
    # catalog key and its values arrive separately, so these match.
    "Give the group a name.": "Donnez un nom au cercle.",
    "There is already a group called {name}.":
        "Il existe déjà un cercle appelé {name}.",
    "Unknown person: {person}.": "Personne inconnue : {person}.",
    "{other} already covers exactly these people. Use that group, or choose "
    "a different set of people for this one.":
        "{other} regroupe déjà exactement ces personnes. Utilisez ce cercle, "
        "ou choisissez d'autres personnes pour celui-ci.",
    "There are already {n} groups, which is as many as this book keeps. "
    "Rename or reuse one instead.":
        "Il y a déjà {n} cercles, soit autant que ce livre en garde. Renommez "
        "ou réutilisez-en un.",

    "Who can see this": "Qui peut la voir",
    "Only {names}": "Seulement {names}",
    "Kept to {names}": "Réservée à {names}",
    "kept to a group": "réservée à un cercle",
    "Stories and people come back; logins never do. Accounts, invitations "
    "and write links stay where they were made, so restoring a zip can't "
    "quietly let someone else's family in.":
        "Les histoires et les personnes reviennent ; jamais les identifiants. "
        "Les comptes, les invitations et les liens d'écriture restent là où "
        "ils ont été créés : restaurer une sauvegarde ne peut donc pas faire "
        "entrer discrètement la famille de quelqu'un d'autre.",
    "Note: some stories are kept to groups you're not in, so a backup you "
    "download leaves them out. A complete backup has to come from someone "
    "who can see every story.":
        "À noter : certaines histoires sont réservées à des cercles dont "
        "vous ne faites pas partie, donc une sauvegarde téléchargée par vous "
        "les laissera de côté. Une sauvegarde complète doit venir de "
        "quelqu'un qui voit toutes les histoires.",
    "Change password": "Changer le mot de passe",
    "Current password": "Mot de passe actuel",
    "New password": "Nouveau mot de passe",
    "Confirm new password": "Confirmer le nouveau mot de passe",
    "Your password has been changed. Any other device you're logged in on "
    "will need to log in again.":
        "Votre mot de passe a été changé. Tout autre appareil connecté devra "
        "se reconnecter.",
    "Write links": "Liens d'écriture",
    "Create link": "Créer un lien",
    "Label (optional)": "Intitulé (facultatif)",
    "e.g. for the recital story": "ex. pour l'histoire du spectacle",
    "Expires after (days, optional)": "Expire après (jours, facultatif)",
    "Never": "Jamais",
    "Copy this now — it won't be shown again:":
        "Copiez-le maintenant — il ne sera plus affiché :",
    "Revoke": "Révoquer",
    "History": "Historique",
    "New account": "Nouveau compte",
    "+ New account": "+ Nouveau compte",
    "Create account": "Créer le compte",
    "Role": "Rôle",
    "No accounts yet.": "Aucun compte pour l'instant.",
    "Pending requests": "Demandes en attente",
    "Review": "Examiner",
    "Review request": "Examiner la demande",
    "Approve": "Approuver",
    "Reject request": "Rejeter la demande",
    "Reset password": "Réinitialiser le mot de passe",
    "Active write-links": "Liens d'écriture actifs",
    "Link": "Lier",
    "Set": "Définir",
    "Family member": "Membre de la famille",
    "— Create a new person —": "— Créer une nouvelle personne —",
    "Name, if creating a new person": "Nom, si vous créez une personne",

    # --- timeline -----------------------------------------------------------
    "No stories yet — this is where your family's memories will live.":
        "Aucune histoire pour l'instant — c'est ici que vivront les "
        "souvenirs de votre famille.",
    "{n} year ago today —": "il y a {n} an aujourd'hui —",
    "{n} years ago today —": "il y a {n} ans aujourd'hui —",
    "turns {n} today": "a {n} ans aujourd'hui",
    "wedding anniversary": "anniversaire de mariage",
    "PACS anniversary": "anniversaire de PACS",
    "anniversary": "anniversaire",
    "{n}-year {kind} today": "{n} ans de {kind} aujourd'hui",
    "Nothing new in {n} month —": "Rien de neuf depuis {n} mois —",
    "Nothing new in {n} months —": "Rien de neuf depuis {n} mois —",
    "a little story?": "une petite histoire ?",
    "Drafts ({n})": "Brouillons ({n})",
    "Archived ({n})": "Archivées ({n})",
    "Search titles, tags, people…": "Rechercher titres, mots-clés, personnes…",
    "Search stories by title, tag, or person":
        "Rechercher une histoire par titre, mot-clé ou personne",
    "Jump to the latest ↓": "Aller à la plus récente ↓",
    "No stories match": "Aucune histoire ne correspond à",
    "Jump to year": "Aller à l'année",
    "A sealed letter · opens {date}": "Une lettre scellée · s'ouvre le {date}",
    "Firsts": "Premières fois",
    "Growing up": "Grandir",
    "Open a page at random": "Ouvrir une page au hasard",
    "Read as a book": "Lire comme un livre",
    "Download as PDF": "Télécharger en PDF",
    "Download as EPUB": "Télécharger en EPUB",
    "Download everything (.zip)": "Tout télécharger (.zip)",
    "Import a backup": "Importer une sauvegarde",

    # --- story --------------------------------------------------------------
    "DRAFT": "BROUILLON",
    "ARCHIVED": "ARCHIVÉE",
    "Listen": "Écouter",
    "Transcript": "Transcription",
    "Story navigation": "Navigation entre les histoires",
    "At random": "Au hasard",
    "A sealed letter": "Une lettre scellée",
    "A sealed letter from {author}": "Une lettre scellée de {author}",
    "It opens on {date}.": "Elle s'ouvre le {date}.",

    # --- drafts / archived --------------------------------------------------
    "Drafts": "Brouillons",
    "No drafts right now.": "Aucun brouillon pour l'instant.",
    "Archived": "Archivées",
    "Nothing archived right now.": "Rien d'archivé pour l'instant.",

    # --- people / tree ------------------------------------------------------
    "New person": "Nouvelle personne",
    "+ New person": "+ Nouvelle personne",
    "Edit person": "Modifier la personne",
    "Family tree": "Arbre généalogique",
    "Almanac": "Almanach",
    "The people who show up again and again — grandparents, godparents, the "
    "family dog — get a page of their own here.":
        "Les personnes qui reviennent encore et encore — grands-parents, "
        "parrains et marraines, le chien de la famille — ont leur page ici.",
    "Friend of": "Ami de",
    "Born {date}": "Né le {date}",
    "Died {date}": "Mort le {date}",
    "Parents": "Parents",
    "Partner": "Conjoint",
    "Partners": "Conjoints",
    "Children": "Enfants",
    "Siblings": "Frères et sœurs",
    "Unions": "Unions",
    "Wedding": "Mariage",
    "PACS": "PACS",
    "Union": "Union",
    "wedding": "mariage",
    "union": "union",
    "Appears in": "Apparaît dans",
    "Link two people in the person editor and the tree will grow here.":
        "Reliez deux personnes dans l'éditeur et l'arbre poussera ici.",
    "Family tree views": "Vues de l'arbre",
    "Friends & others": "Amis et autres",
    "friend of": "ami de",
    "Other family": "Autre famille",

    # --- firsts / growth / almanac -----------------------------------------
    'Give any story a milestone label in the editor — "First steps", '
    '"First word" — and it\'ll appear here, in the order it happened.':
        "Donnez à une histoire un intitulé de première fois dans l'éditeur — "
        "« Premiers pas », « Premier mot » — et elle apparaîtra ici, dans "
        "l'ordre où c'est arrivé.",
    "Set {var} in your configuration to turn this on — the photo closest to "
    "each birthday, one per year.":
        "Définissez {var} dans votre configuration pour activer ceci — la "
        "photo la plus proche de chaque anniversaire, une par an.",
    "Add a cover photo to a story and it'll take its place here — the photo "
    "nearest each birthday, one per year, watching them grow in one glance.":
        "Ajoutez une photo de couverture à une histoire et elle prendra sa "
        "place ici — la photo la plus proche de chaque anniversaire, une par "
        "an, pour les voir grandir d'un seul coup d'œil.",
    "Newborn": "Nouveau-né",
    "Turning {n}": "{n} ans",
    "Add a birth, death, wedding, or PACS date to someone in the person "
    "editor, and it'll take its place here — a family's dates, month by "
    "month, the way a real record book keeps them.":
        "Ajoutez une date de naissance, de décès, de mariage ou de PACS à "
        "quelqu'un dans l'éditeur, et elle prendra sa place ici — les dates "
        "d'une famille, mois par mois, comme dans un vrai livre de famille.",
    "born, {year}": "né, {year}",
    "died, {year}": "mort, {year}",

    # --- book ---------------------------------------------------------------
    "Stories from {year}": "Histoires de {year}",
    "Stories from {start} to {end}": "Histoires de {start} à {end}",
    "Print / save as PDF": "Imprimer / enregistrer en PDF",

    # --- editor -------------------------------------------------------------
    "New story": "Nouvelle histoire",
    "Edit story": "Modifier l'histoire",
    "New instant": "Nouvel instant",
    "Untitled": "Sans titre",
    "Seal until": "Sceller jusqu'au",
    "Tags, comma separated": "Mots-clés, séparés par des virgules",
    "A first? (e.g. First steps)": "Une première fois ? (ex. Premiers pas)",
    "Who's in this story": "Qui est dans cette histoire",
    "Search names…": "Rechercher un nom…",
    "Search {label}": "Rechercher {label}",
    "Draft": "Brouillon",
    "Archive": "Archiver",
    "Another idea": "Une autre idée",
    "Sources": "Sources",
    "+ Add source": "+ Ajouter une source",
    "Photo": "Photo",
    "Take a photo": "Prendre une photo",
    "Add a photo": "Ajouter une photo",
    "Change photo": "Changer la photo",
    "No photo yet": "Pas encore de photo",
    "Voice": "Voix",
    "Record": "Enregistrer",
    "Pause": "Pause",
    "Stop": "Arrêter",
    "View history": "Voir l'historique",
    "You have an unsaved draft from": "Vous avez un brouillon non enregistré du",
    "Restore it": "Le restaurer",
    "Discard": "Abandonner",
    "One line…": "Une ligne…",
    "Name": "Nom",
    "Relation (e.g. your grandmother)": "Lien (ex. ta grand-mère)",
    "Born": "Naissance",
    "Died": "Décès",
    "Byline color": "Couleur de signature",
    "Zoom": "Zoom",
    "Zoom in": "Zoomer",
    "Zoom out": "Dézoomer",
    "Drag the photo to reposition it.":
        "Faites glisser la photo pour la repositionner.",
    "Use this photo": "Utiliser cette photo",
    "Sepia tone": "Teinte sépia",
    "Family": "Famille",
    "Parents (up to two)": "Parents (deux au maximum)",
    "+ Add union": "+ Ajouter une union",
    "Gender": "Genre",
    "Unset": "Non défini",
    "Add another person and you'll be able to link parents, a partner, and "
    "gender here — those pickers need someone else to point at.":
        "Ajoutez une autre personne et vous pourrez relier parents, conjoint "
        "et genre ici — ces sélecteurs ont besoin de quelqu'un d'autre.",

    # --- history ------------------------------------------------------------
    "Back to editor": "Retour à l'éditeur",
    "History for “{title}”": "Historique de « {title} »",
    "No earlier versions yet — every future save will be recorded here.":
        "Aucune version antérieure — chaque enregistrement futur sera noté ici.",

    # --- import -------------------------------------------------------------
    'Restore stories from a zip downloaded via "Download everything (.zip)". '
    "This only works if none of the zip's stories already exist here — if "
    "anything would collide, nothing is changed and you'll see an error below.":
        "Restaurez des histoires depuis un zip téléchargé via « Tout "
        "télécharger (.zip) ». Cela ne fonctionne que si aucune des histoires "
        "du zip n'existe déjà ici — en cas de conflit, rien n'est modifié et "
        "une erreur s'affiche ci-dessous.",
    "Choose a backup .zip": "Choisir un fichier .zip",

    # --- write links / delegate --------------------------------------------
    "Write for {name}": "Écrire pour {name}",
    "Your story is added straight to their book. You won't see anything else "
    "here, and this page won't show it back to you afterward.":
        "Votre histoire est ajoutée directement à leur livre. Vous ne verrez "
        "rien d'autre ici, et cette page ne vous la remontrera pas ensuite.",
    "Title": "Titre",
    "Date": "Date",
    "Story": "Histoire",
    "Add this story": "Ajouter cette histoire",
    "Thank you": "Merci",
    "Your story for {name} has been added to the book.":
        "Votre histoire pour {name} a été ajoutée au livre.",
    "Link not valid": "Lien non valide",
    "This link isn't valid anymore — it may have already been used, revoked, "
    "or expired. Ask whoever sent it to you for a new one.":
        "Ce lien n'est plus valide — il a peut-être déjà été utilisé, révoqué "
        "ou expiré. Demandez-en un nouveau à la personne qui vous l'a envoyé.",

    # --- errors -------------------------------------------------------------
    "Not found": "Introuvable",
    "That page doesn't exist, or it never did.":
        "Cette page n'existe pas, ou n'a jamais existé.",
    "Back to the timeline": "Retour au fil du temps",
    "That page had gone stale": "Cette page n'était plus à jour",
    "For safety this app refuses a form it can't match to your current "
    "session. Log in again and redo that last step — nothing was saved or "
    "lost.":
        "Par sécurité, cette application refuse un formulaire qu'elle ne peut "
        "pas rattacher à votre session. Reconnectez-vous et refaites cette "
        "dernière étape — rien n'a été enregistré ni perdu.",
    "This usually means the reverse proxy in front of this app isn't "
    "forwarding the address you typed. Whoever set it up should check that it "
    "sends X-Forwarded-Host and X-Forwarded-Proto, and that "
    "STORYBOOK_TRUSTED_PROXIES is set.":
        "Cela signifie en général que le proxy inverse placé devant cette "
        "application ne transmet pas l'adresse que vous avez saisie. La "
        "personne qui l'a configuré doit vérifier qu'il envoie "
        "X-Forwarded-Host et X-Forwarded-Proto, et que "
        "STORYBOOK_TRUSTED_PROXIES est défini.",
    "That file is too big": "Ce fichier est trop volumineux",
    "The upload limit is 128 MB. Try a smaller file, or copy it straight into "
    "the stories folder instead.":
        "La limite d'envoi est de 128 Mo. Essayez un fichier plus petit, ou "
        "copiez-le directement dans le dossier des histoires.",
    "File too large (max 128 MB).": "Fichier trop volumineux (128 Mo maximum).",
    "Your session expired. Reload the page and try again.":
        "Votre session a expiré. Rechargez la page et réessayez.",
    "Something was wrong with that request": "Cette requête posait problème",
    "The app couldn't make sense of what the browser sent. Reload the page "
    "and try again.":
        "L'application n'a pas compris ce que le navigateur a envoyé. "
        "Rechargez la page et réessayez.",
    "Not allowed": "Non autorisé",
    "You don't have access to that.": "Vous n'avez pas accès à cela.",
    "Too many attempts": "Trop de tentatives",
    "Wait a few minutes and try again.":
        "Attendez quelques minutes et réessayez.",
    "Too many attempts. Try again in about {n} minute.":
        "Trop de tentatives. Réessayez dans environ {n} minute.",
    "Too many attempts. Try again in about {n} minutes.":
        "Trop de tentatives. Réessayez dans environ {n} minutes.",
    "Something went wrong": "Quelque chose s'est mal passé",
    "That's a fault in the app, not anything you did. Your stories are files "
    "on disk and are unaffected.":
        "C'est un défaut de l'application, pas quelque chose que vous avez "
        "fait. Vos histoires sont des fichiers sur le disque et ne sont pas "
        "touchées.",
    "Not found.": "Introuvable.",

    # --- ages (F3) ----------------------------------------------------------
    "before you were born": "avant ta naissance",
    "{n} day old": "{n} jour",
    "{n} days old": "{n} jours",
    "{n} month old": "{n} mois",
    "{n} months old": "{n} mois",
    "{n} year old": "{n} an",
    "{n} years old": "{n} ans",

    # --- help page (F42) ----------------------------------------------------
    # The page is a glossary: one term, one line. Terms already translated
    # elsewhere (Story, Draft, Archived, Firsts, Growing up, History...) are
    # not repeated here — they resolve through their existing entry.
    "What each word here means, in one line each. Nothing is required "
    "reading, and nothing can be lost by accident: every save keeps the one "
    "before it.":
        "Ce que veut dire chaque mot d'ici, une ligne chacun. Rien n'est "
        "obligatoire à lire, et rien ne peut être perdu par accident : chaque "
        "enregistrement garde le précédent.",

    "Instant": "Instant",
    "A dated entry — a title, the day it happened, and as much writing and as "
    "many photos as you like.":
        "Une entrée datée — un titre, le jour où c'est arrivé, et autant de "
        "texte et de photos que vous voulez.",
    "A photo and one line, for a moment that doesn't need a whole story.":
        "Une photo et une ligne, pour un moment qui n'a pas besoin de toute "
        "une histoire.",
    "Unfinished. Only the people who write in this book can see it.":
        "Pas terminée. Seules les personnes qui écrivent dans ce livre la "
        "voient.",
    "Sealed letter": "Lettre scellée",
    "Hidden from the timeline — from you too — until the date you set.":
        "Cachée du fil du temps — de vous aussi — jusqu'à la date que vous "
        "avez choisie.",
    "Milestone": "Première fois",
    "A short label marking a real first (first steps, first word). It joins "
    "the Firsts page.":
        "Un court intitulé pour une vraie première fois (premiers pas, premier "
        "mot). Elle rejoint la page Premières fois.",
    "Put aside without deleting: off the timeline, still there on the "
    "Archived page.":
        "Mise de côté sans être supprimée : hors du fil du temps, toujours là "
        "sur la page Archivées.",
    "Facing a blank page? A new story opens with an idea to start from — ask "
    "for another until one fits.":
        "Devant la page blanche ? Une nouvelle histoire s'ouvre avec une idée "
        "pour démarrer — demandez-en une autre jusqu'à ce qu'une vous aille.",

    "Who can read a story": "Qui peut lire une histoire",
    "Every story is for the whole family, unless you keep it to a group.":
        "Chaque histoire est pour toute la famille, sauf si vous la réservez à "
        "un cercle.",
    "Group": "Cercle",
    "A named handful of people. Pick one in the editor and only those people "
    "— and you, always — can read that story.":
        "Une poignée de personnes, sous un nom. Choisissez-en un dans "
        "l'éditeur et seules ces personnes — et vous, toujours — pourront lire "
        "cette histoire.",
    "Making one": "En créer un",
    "Anyone can, from Groups in the nav. It puts you in the group, and the "
    "people in a group are the ones who can change it.":
        "Tout le monde peut le faire, depuis Cercles dans la navigation. Cela "
        "vous met dans le cercle, et ce sont les personnes qui en font partie "
        "qui peuvent le modifier.",
    "Widening one": "En élargir un",
    "Adding someone opens every story kept to that group, including other "
    "people's — the page tells you how many.":
        "Ajouter quelqu'un ouvre toutes les histoires réservées à ce cercle, y "
        "compris celles des autres — la page vous dit combien.",

    "Person": "Personne",
    "Family and friends you can tag in a story, each with a page listing the "
    "stories they appear in.":
        "La famille et les amis que vous pouvez marquer dans une histoire, "
        "chacun avec une page qui liste celles où ils apparaissent.",
    "Link parents and partners and it works the relationships out on its own "
    "— you never type a kinship word like great-aunt yourself.":
        "Reliez parents et conjoints et il déduit tout seul les liens — vous "
        "n'écrivez jamais un mot de parenté comme « grand-tante » vous-même.",
    "Life dates": "Dates de la vie",
    "A birthday, a wedding or PACS, a death. They surface on the timeline on "
    "the day, and fill the Almanac month by month.":
        "Un anniversaire, un mariage ou un PACS, un décès. Ils remontent sur "
        "le fil du temps le jour venu, et remplissent l'Almanach mois par "
        "mois.",

    "Everything in order, newest first, with what happened on this day in an "
    "earlier year when there's a match.":
        "Tout dans l'ordre, le plus récent en haut, avec ce qui s'est passé ce "
        "jour-là une année plus tôt quand il y a une correspondance.",
    "One page from the past, unannounced.":
        "Une page du passé, sans prévenir.",
    "Every milestone, in the order it happened.":
        "Toutes les premières fois, dans l'ordre où elles sont arrivées.",
    "The story photo nearest each birthday, year beside year (needs the "
    "child's birth date set).":
        "La photo la plus proche de chaque anniversaire, année après année "
        "(demande que la date de naissance de l'enfant soit renseignée).",
    "Book and EPUB": "Livre et EPUB",
    "The whole book as flowing pages — to print, to save as a PDF, or to read "
    "on an e-reader.":
        "Tout le livre en pages continues — à imprimer, à enregistrer en PDF, "
        "ou à lire sur une liseuse.",

    "Photos and voice memos": "Photos et mémos vocaux",
    "Anywhere a photo can go, add one from your files or take it there and "
    "then. Any story can also carry a short recording — a child's own voice, "
    "or someone telling the story out loud.":
        "Partout où une photo peut aller, ajoutez-en une depuis vos fichiers "
        "ou prenez-la sur le moment. Chaque histoire peut aussi porter un "
        "court enregistrement — la voix de l'enfant, ou quelqu'un qui raconte "
        "à voix haute.",
    "The camera and the recorder need a secure connection (https). If those "
    "buttons aren't there, that's why — ask whoever set this up.":
        "L'appareil photo et l'enregistreur demandent une connexion sécurisée "
        "(https). Si ces boutons ne sont pas là, c'est pour cette raison — "
        "demandez à la personne qui a installé ce livre.",

    "Your account": "Votre compte",
    "Your own name and password rather than a shared one. Change it from "
    "Account in the nav.":
        "Votre propre nom et votre propre mot de passe, plutôt qu'un mot de "
        "passe partagé. Changez-le depuis Compte dans la navigation.",
    "Write link": "Lien d'écriture",
    "A one-off link letting someone add a single story without an account of "
    "their own.":
        "Un lien à usage unique qui laisse quelqu'un ajouter une seule "
        "histoire sans avoir de compte.",
    "Invitation": "Invitation",
    "How someone new gets in: an invite code from an admin, or a request an "
    "admin approves.":
        "Comment une nouvelle personne entre : un code d'invitation donné par "
        "un administrateur, ou une demande qu'un administrateur accepte.",

    "Every save keeps the previous version; a story's History page puts an "
    "older one back.":
        "Chaque enregistrement garde la version précédente ; la page "
        "Historique d'une histoire en remet une ancienne.",
    "Backup": "Sauvegarde",
    "Download everything (.zip) from the timeline's footer; Import a backup "
    "restores it.":
        "Tout télécharger (.zip) depuis le pied du fil du temps ; Importer une "
        "sauvegarde la restaure.",
    "The files themselves": "Les fichiers eux-mêmes",
    "Plain text and photos in folders — readable with or without this app, on "
    "any computer.":
        "Du texte simple et des photos dans des dossiers — lisibles avec ou "
        "sans cette application, sur n'importe quel ordinateur.",

    # Validation messages raised as plain strings by accounts.py/people.py
    # and translated at the one place they're shown (the flash call).
    "Passwords don't match.": "Les mots de passe ne correspondent pas.",
    "New passwords don't match.":
        "Les nouveaux mots de passe ne correspondent pas.",
    "Current password is incorrect.": "Le mot de passe actuel est incorrect.",
    "Usernames must be 3-32 characters: lowercase letters, numbers, hyphens.":
        "Le nom d'utilisateur doit faire 3 à 32 caractères : minuscules, "
        "chiffres, tirets.",
    "That family member already has an account.":
        "Ce membre de la famille a déjà un compte.",
    "Can't demote the only remaining admin.":
        "Impossible de rétrograder le dernier administrateur.",
    "Can't disable the only remaining admin.":
        "Impossible de désactiver le dernier administrateur.",
    "Pick an existing family member, or enter a name for a new one.":
        "Choisissez un membre de la famille existant, ou saisissez un nom pour "
        "en créer un.",
    "Provide exactly one of an existing person or a new person's name.":
        "Indiquez soit une personne existante, soit le nom d'une nouvelle — "
        "pas les deux.",
    "Enter a valid date.": "Saisissez une date valide.",

    # --- admin odds and ends -------------------------------------------------
    "(no label)": "(sans intitulé)",
    "Note:": "Note :",
    "One use only": "Usage unique",
    "Reject": "Rejeter",
    "Disable": "Désactiver",
    "Enable": "Activer",
    "{name} (current)": "{name} (actuel)",
    "{name} requested the username {username}.":
        "{name} a demandé le nom d'utilisateur {username}.",
    "Reset {name}'s password": "Réinitialiser le mot de passe de {name}",
    "Share a link with someone so they can write one story for you — no "
    "account, no password of their own. They can't see anything else in the "
    "book.":
        "Partagez un lien avec quelqu'un pour qu'il écrive une histoire pour "
        "vous — sans compte, sans mot de passe. Il ne voit rien d'autre du "
        "livre.",
    "They'll need this new password next time they log in — any device "
    "they're already logged in on will need to log in again too.":
        "Il lui faudra ce nouveau mot de passe à la prochaine connexion — tout "
        "appareil déjà connecté devra se reconnecter aussi.",
    # Account status words and role names, rendered straight from data.
    "active": "actif",
    "revoked": "révoqué",
    "expired": "expiré",
    "used": "utilisé",
    "disabled": "désactivé",
    "pending": "en attente",
    # The "family" role capitalizes to "Family", which already appears
    # above as the person editor's fieldset legend — same word, same
    # translation, so it isn't repeated here.
    "Admin": "Administrateur",

    "Writing a memory": "Écrire un souvenir",
    "The cast — people and the family tree":
        "Les personnages — les personnes et l'arbre généalogique",
    "Reading it back": "Le relire",
    "Photos": "Photos",
    "Voice memos": "Mémos vocaux",
    "Family accounts": "Comptes de famille",
    "Keeping it safe": "Le garder en sécurité",

    # --- strings only static/js/i18n.js reads (see i18n.py's JS_STRINGS) ---
    "Turn the firelight off": "Éteindre la lueur du feu",
    "Turn the firelight on": "Allumer la lueur du feu",
    "Close": "Fermer",
    "Flip": "Changer",
    "Switch camera": "Changer de caméra",
    "Take photo": "Prendre la photo",
    "Retake": "Reprendre",
    "Use photo": "Utiliser la photo",
    "Camera access was denied. You can still add a photo from your files.":
        "L'accès à la caméra a été refusé. Vous pouvez toujours ajouter une "
        "photo depuis vos fichiers.",
    "No camera found on this device.": "Aucune caméra trouvée sur cet appareil.",
    "The camera is busy in another app. Close it and try again.":
        "La caméra est utilisée par une autre application. Fermez-la et "
        "réessayez.",
    "Could not start the camera.": "Impossible de démarrer la caméra.",
    "The camera isn't ready yet — try again in a moment.":
        "La caméra n'est pas encore prête — réessayez dans un instant.",
    "Could not take that photo. Try again.":
        "Impossible de prendre cette photo. Réessayez.",
    "Microphone access was denied.": "L'accès au microphone a été refusé.",
    "Could not save the recording.": "Impossible d'enregistrer l'audio.",
    "Could not delete the recording.": "Impossible de supprimer l'enregistrement.",
    "Recording stopped when the page went to the background. Everything "
    "recorded up to then has been saved.":
        "L'enregistrement s'est arrêté quand la page est passée en "
        "arrière-plan. Tout ce qui avait été enregistré est sauvegardé.",
    "Recording stopped when the microphone became unavailable. Everything "
    "recorded up to then has been saved.":
        "L'enregistrement s'est arrêté quand le microphone est devenu "
        "indisponible. Tout ce qui avait été enregistré est sauvegardé.",
    "Recording stopped when the microphone went silent. Everything recorded "
    "up to then has been saved.":
        "L'enregistrement s'est arrêté quand le microphone est devenu "
        "muet. Tout ce qui avait été enregistré est sauvegardé.",
    "The recording was interrupted. Everything recorded up to then has been "
    "saved.":
        "L'enregistrement a été interrompu. Tout ce qui avait été "
        "enregistré est sauvegardé.",
    "Could not reach the server. The recording is still here — keep this "
    "page open and it will try again.":
        "Impossible de joindre le serveur. L'enregistrement est toujours "
        "là — gardez cette page ouverte et il réessaiera.",
    "Adding the photo…": "Ajout de la photo…",
    "Could not add that photo.": "Impossible d'ajouter cette photo.",
    "Resume": "Reprendre",
    "Saving…": "Enregistrement…",
    "https://...": "https://...",
    "Since": "Depuis",
    "Until (optional)": "Jusqu'à (optionnel)",
    "Remove source": "Supprimer la source",
    "Remove union": "Supprimer l'union",
    "Recenter": "Recentrer",
    "Recenter the family tree": "Recentrer l'arbre généalogique",
    "Could not load the family tree.":
        "Impossible de charger l'arbre généalogique.",
    "Everyone": "Tout le monde",
    "Import failed.": "Échec de l'import.",
    "Could not import. Please check your connection and try again.":
        "Impossible d'importer. Vérifiez votre connexion et réessayez.",
    "Imported {n} story. Reloading…": "{n} histoire importée. Rechargement…",
    "Imported {n} stories. Reloading…": "{n} histoires importées. Rechargement…",
    "Add a partner above first.": "Ajoutez d'abord un·e partenaire ci-dessus.",
}
