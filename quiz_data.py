# Dati delle domande per il quiz "AI Quest"
# Organizzati per zone seguendo lo scaffold del progetto

QUIZ_QUESTIONS = [
    # ZONA 1: Foresta delle Basi (Domande 1-2)
    {
        "zone": 1,
        "zone_order": 1,
        "text": "Cos'è una CNN (Convolutional Neural Network)?",
        "option_a": "Un tipo di connessione internet molto veloce",
        "option_b": "Una rete neurale specializzata nel processare dati con struttura a griglia, come le immagini",
        "option_c": "Un algoritmo per comprimere file",
        "option_d": "Un database per salvare foto",
        "correct_answer": "b",
        "explanation": "Una CNN è progettata per 'vedere' pattern nelle immagini. Usa filtri che scorrono sull'immagine per riconoscere bordi, forme e texture. È come avere tanti piccoli detective che cercano indizi diversi nella stessa foto! 🔍"
    },
    {
        "zone": 1,
        "zone_order": 2,
        "text": "Perché usare una CNN invece di una normale rete neurale Dense per riconoscere immagini?",
        "option_a": "Le CNN sono più economiche da addestrare",
        "option_b": "Le reti Dense non funzionano con i numeri",
        "option_c": "Le CNN preservano le relazioni spaziali tra i pixel e hanno meno parametri grazie alla condivisione dei pesi",
        "option_d": "Non c'è differenza, è solo una moda",
        "correct_answer": "c",
        "explanation": "Una rete Dense tratterebbe ogni pixel come indipendente, perdendo l'informazione che 'questo pixel è vicino a quest'altro'. La CNN invece capisce che i pixel vicini sono correlati. In più, usando lo stesso filtro su tutta l'immagine, ha molti meno parametri da imparare. Efficienza + intelligenza spaziale! 🧠"
    },
    
    # ZONA 2: Montagna dei Dati (Domanda 3)
    {
        "zone": 2,
        "zone_order": 1,
        "text": "Il dataset MNIST contiene immagini di cifre scritte a mano. Qual è la dimensione di ogni immagine?",
        "option_a": "32x32 pixel a colori (RGB)",
        "option_b": "28x28 pixel in scala di grigi",
        "option_c": "64x64 pixel in bianco e nero",
        "option_d": "224x224 pixel a colori",
        "correct_answer": "b",
        "explanation": "MNIST usa immagini 28x28 pixel con un solo canale (scala di grigi, valori 0-255). È piccolo ma perfetto per imparare! Input shape in Keras: (28, 28, 1). Ricorda: 28x28 = 784 pixel totali, come una griglia di appunti delle superiori! 📝"
    },
    
    # ZONA 3: Tempio della Convoluzione (Domande 4-5)
    {
        "zone": 3,
        "zone_order": 1,
        "text": "Cosa fa un layer Conv2D in una CNN?",
        "option_a": "Comprime l'immagine per occupare meno memoria",
        "option_b": "Applica filtri che scorrono sull'immagine per estrarre feature come bordi e pattern",
        "option_c": "Converte l'immagine da colori a bianco e nero",
        "option_d": "Raddrizza le immagini storte",
        "correct_answer": "b",
        "explanation": "Conv2D applica piccoli filtri (es. 3x3) che 'scivolano' su tutta l'immagine. Ogni filtro impara a riconoscere una feature specifica: uno trova i bordi verticali, uno quelli orizzontali, uno le curve. Conv2D è il detective che cerca indizi in ogni angolo dell'immagine! 🕵️"
    },
    {
        "zone": 3,
        "zone_order": 2,
        "text": "Qual è lo scopo principale del MaxPooling2D?",
        "option_a": "Aumentare la risoluzione dell'immagine",
        "option_b": "Ridurre le dimensioni spaziali mantenendo le feature più importanti",
        "option_c": "Aggiungere colori all'immagine",
        "option_d": "Mescolare i pixel casualmente",
        "correct_answer": "b",
        "explanation": "MaxPooling prende una finestra (es. 2x2) e tiene solo il valore massimo, scartando il resto. Questo riduce le dimensioni (meno calcoli!) e rende la rete più robusta a piccole variazioni. MaxPooling è il filtro che butta via il rumore e tiene solo il meglio! 🏆"
    },
    
    # ZONA 4: Ponte del Flatten (Domanda 6)
    {
        "zone": 4,
        "zone_order": 1,
        "text": "Perché serve Flatten() prima di un layer Dense()?",
        "option_a": "Per rendere l'immagine più bella",
        "option_b": "Perché Dense richiede input 1D, mentre l'output di Conv2D/MaxPooling è 2D/3D",
        "option_c": "Per velocizzare il training",
        "option_d": "Flatten è opzionale, si può omettere",
        "correct_answer": "b",
        "explanation": "Dopo Conv2D e MaxPooling hai ancora una struttura 3D (altezza × larghezza × filtri). Ma Dense vuole un vettore 1D! Flatten 'schiaccia' tutto in una linea. Se hai un output 7×7×64, Flatten lo trasforma in un vettore di 3136 elementi. Flatten schiaccia tutto come una frittata! 🥞"
    },
    
    # ZONA 5: Castello della Classificazione (Domande 7-10)
    {
        "zone": 5,
        "zone_order": 1,
        "text": "Quanti neuroni deve avere l'ultimo layer Dense per classificare le cifre MNIST (0-9)?",
        "option_a": "model.add(Dense(1, activation='softmax'))",
        "option_b": "model.add(Dense(10, activation='softmax'))",
        "option_c": "model.add(Dense(28, activation='softmax'))",
        "option_d": "model.add(Dense(784, activation='softmax'))",
        "correct_answer": "b",
        "explanation": "Devi classificare 10 classi diverse (cifre 0, 1, 2... fino a 9), quindi servono esattamente 10 neuroni. Ogni neurone rappresenta la probabilità che l'immagine sia quella cifra. 10 cifre = 10 neuroni, semplice! 🔢"
    },
    {
        "zone": 5,
        "zone_order": 2,
        "text": "Quale activation function è corretta nell'ultimo layer per una classificazione multi-classe come MNIST?",
        "option_a": "Dense(10, activation='relu')",
        "option_b": "Dense(10, activation='sigmoid')",
        "option_c": "Dense(10, activation='softmax')",
        "option_d": "Dense(10, activation='tanh')",
        "correct_answer": "c",
        "explanation": "Softmax trasforma gli output in probabilità che sommano a 1. Se il modello è sicuro che sia un '7', l'output potrebbe essere [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.92, 0.01, 0.01]. Softmax è l'arbitro che assegna le probabilità! ⚖️"
    },
    {
        "zone": 5,
        "zone_order": 3,
        "text": "Quale struttura di CNN è corretta per classificare MNIST?",
        "option_a": "Sequential([Dense(128), Conv2D(32), Flatten(), Dense(10)])",
        "option_b": "Sequential([Conv2D(32), MaxPooling2D(), Flatten(), Dense(10, activation='softmax')])",
        "option_c": "Sequential([Flatten(), Conv2D(32), Dense(10)])",
        "option_d": "Sequential([MaxPooling2D(), Dense(10), Conv2D(32), Flatten()])",
        "correct_answer": "b",
        "explanation": "L'ordine è fondamentale! Prima estrai features con Conv2D, riduci con MaxPooling, appiattisci con Flatten, e infine classifica con Dense. L'ordine conta sempre: Conv → Pool → Flatten → Dense. Come una catena di montaggio! ⚙️"
    },
    {
        "zone": 5,
        "zone_order": 4,
        "text": "Quale loss function è corretta per addestrare una CNN su MNIST?",
        "option_a": "model.compile(loss='binary_crossentropy')",
        "option_b": "model.compile(loss='categorical_crossentropy')",
        "option_c": "model.compile(loss='mean_squared_error')",
        "option_d": "model.compile(loss='hinge')",
        "correct_answer": "b",
        "explanation": "categorical_crossentropy è per classificazione multi-classe con one-hot encoding. Se usi label come interi (0,1,2...) usa sparse_categorical_crossentropy. MSE è per regressione, binary_crossentropy per 2 classi sole. Categorie multiple = categorical_crossentropy! 🎯"
    }
]

ITEMS = {
    1: {"id": "boots", "name": "Stivali del Principiante", "emoji": "🥾"},
    2: {"id": "backpack", "name": "Zaino dei Dati", "emoji": "🎒"},
    3: {"id": "sword", "name": "Spada dei Filtri", "emoji": "⚔️"},
    4: {"id": "shield", "name": "Scudo Dimensionale", "emoji": "🛡️"},
    5: {"id": "crown", "name": "Corona del Maestro CNN", "emoji": "👑"},
}

ZONE_NAMES = {
    1: "Foresta delle Basi",
    2: "Monti dei Dati",
    3: "Tempio della Convoluzione",
    4: "Ponte del Flatten",
    5: "Castello della Classificazione"
}
