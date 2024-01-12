def list():
    list1()
    list2()
    list3()
    list4()
    list5()
    listplot()


def list1():
    print(f"REDES NEURONALES\n"
          f"0 - list1()\n"
          f"1 - pasos1()\n"
          f"2 - carga1()\n"
          f"3 - hold1()\n"
          f"4 - norm1()\n"
          f"5 - ini1()\n"
          f"6 - forwd1()\n"
          f"7 - cost1()\n"
          f"8 - grad1()\n"
          f"9 - fmin1()\n"
          f"10 - unroll1()\n"
          f"11 - pred1()\n"
          f"12 - nnsk1()\n"
          )


def list2():
    print(f"RECOMENDACION\n"
          f"0 - list2()\n"
          f"1 - pasos2()\n"
          f"2 - carga2()\n"
          f"3 - rank2()\n"
          f"4 - cost2()\n"
          f"5 - grad2()\n"
          f"6 - fmin2()\n"
          f"7 - recom2()\n"
          f"8 - simi2()\n"
          f"9 - km2()\n"
          f"10 - checkG2()\n"
          f"11 - ejeEB()\n"
          f"12 - funcionesEPD()\n")

def list3():
    print(f"CLUSTERING\n"
          f"0 - list3()\n"
          f"1 - pasos3()\n"
          f"2 - carga3()\n"
          f"3 - fcc3()\n"
          f"4 - compc3()\n"
          f"5 - kmean3()\n"
          f"6 - randini3()\n"
          f"7 - elbow3()\n"
          f"8 - clustsk3()\n")

def list4():
    print(f"Lineal y Logistica\n"
          f"0 - list4()\n"
          f"1 - rlineal4()\n"
          f"2 - rlogi4()\n")

def list5():
    print(f"Busquedas\n"
          f"0 - misioneros()\n"
          f"1 - cantaros()\n"
          f"2 - laberinto()\n"
          f"3 - laberinto2()\n")


def listplot():
    print(f"PLOT\n"
          f"0 - listplot()\n"
          f"1 - plot()\n"
          f"2 - frontera()\n"
          f"3 - seaborn()\n")

def pasos1():
    print("1 - Carga de datos\n"
          "2 - Holdout\n"
          "3 - Normaliza\n"
          "4 - Inicializa las thetas (pesos)\n"
          "5 - Forward\n"
          "6 - Coste\n"
          "7 - Gradiente\n"
          "8 - Fmin\n"
          "9 - Desenrolla el fmin\n"
          "10 - Normaliza X-test\n"
          "11 - Predice\n")

def pasos2():
    print("1 - Carga de datos\n"
          "2 - Ranking de peliculas\n"
          "3 - Coste\n"
          "4 - Gradiente\n"
          "5 - Fmin\n"
          "6 - Recomendacion usuario\n"
          "7 - Peliculas similares\n"
          "8 - Kmeans\n"
          "9 - checknngradients\n")




def carga1():
    string = '''
        # Cargar los datos 
        data = pd.read_csv("drivers_behavior.csv")
        y = pd.DataFrame(data['Target'])
        X = data.drop(['Target'], axis=1)
        
        # Definición parámetros RED NEURONAL
        input_layer_size = 60
        hidden_layer_size1 = 50
        hidden_layer_size2 = 25
        num_labels = 4
    '''

    print(string)


def hold1():
    string = '''
        def holdout(X, y, percentage=0.75):
            X_training = X.sample(round(percentage * len(X)))

            y_training = y.iloc[X_training.index]

            X_test = X.iloc[~X.index.isin(X_training.index)]
            y_test = y.iloc[~y.index.isin(y_training.index)]

            X_training = X_training.reset_index(drop=True)
            y_training = y_training.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)
            y_test = y_test.reset_index(drop=True)

            X_training = X_training.to_numpy()
            y_training = y_training.to_numpy()
            X_test = X_test.to_numpy()
            y_test = y_test.to_numpy()

            return X_training, y_training, X_test, y_test
      '''

    print(string)


def norm1():
    string = '''
        # Main
        X_train, mean, std = normalize(X, X_train)
        # Funcion
        def normalize(X, X_training):
            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)
            normal = []
            for i in range(X_training.shape[0]):
                x = X_training[i] - mean
                x = x / std
                normal.append(x)

            return normal, mean, std
      '''

    print(string)


def ini1():
    string = '''
        # Main
        #añadiendo bias
        theta1 = randInitializeWeights(input_layer_size, hidden_layer_size1)
        theta2 = randInitializeWeights(hidden_layer_size1, hidden_layer_size2)
        theta3 = randInitializeWeights(hidden_layer_size2, num_labels)

        # Funcion
        def randInitializeWeights(capa_entrada, capa_salida):
              epsilon_init = 0.12
              W = np.random.rand(capa_salida, capa_entrada+1) * 2 * epsilon_init - epsilon_init
              return W
      '''

    print(string)


def forwd1():
    string = '''
        def forward(theta1, theta2, theta3, X):
            #Variables necesarias
            m = len(X)
            ones = np.ones((m, 1))

            a1 = np.hstack((ones, X))

            a2 = sigmoid(a1 @ theta1.T)
            a2 = np.hstack((ones, a2))

            a3 = sigmoid(a2 @ theta2.T)
            a3 = np.hstack((ones, a3))

            a4 = sigmoid(a3 @ theta3.T)

            return a1, a2, a3, a4
      '''

    print(string)


def cost1():
    string = '''
        # Main
        nn_params = np.hstack((theta1.ravel(order='F'), theta2.ravel(order='F'), theta3.ravel(order='F')))
        J = nnCostFunctionReg(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_train, y_train, lambda_param = 0.01)
        # Funcion
        def nnCostFunctionReg(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y, lambda_param):
            m = len(X)
        
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2 * (hidden_layer_size1+1))
            theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
            inicio = fin
            theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')
        
            a1, a2, a3, h = forward(theta1, theta2, theta3, X)
            #Getdummies solo si es multiclase
            y_d = pd.get_dummies(y.flatten())
        
            temp1 = np.multiply(y_d, np.log(h))
            temp2 = np.multiply(1 - y_d, np.log(1 - h))
            temp3 = np.sum(temp1 + temp2)
        
            J = -np.sum(temp3) / m
            reg_term = (np.sum(np.square(theta1[:, 1:])) + np.sum(np.square(theta2[:, 1:])) + np.sum(np.square(theta3[:, 1:]))) * lambda_param / (2 * m)
            J += reg_term
        
            return J
      '''

    print(string)


def grad1():
    string = '''
        # Main
        lambda_param = 0
        comprobacion = checkNNGradients(lambda_param)
        gradiente = nnGradFunctionReg(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_train, y_train, lambda_param)
        # Funcion
        def nnGradFunctionReg(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X, y, lambda_):
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size+1)
            theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size+1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2 * (hidden_layer_size1+1))
            theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1+1), order='F')
            inicio = fin
            theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2+1), order='F')
        
            m = len(y)
            #Solo si es multiclase
            y_d = pd.get_dummies(y.flatten())
            a1, a2, a3, a4 = forward(theta1, theta2, theta3, X)
        
            d4 = a4 - y_d
            d3 = np.multiply(np.dot(d4, theta3), np.multiply(a3, 1 - a3))
            d2 = np.multiply(np.dot(d3[:, 1:], theta2), np.multiply(a2, 1 - a2))
            d3 = d3[:, 1:]
            d2 = d2[:, 1:]
        
            delta1 = d2.T @ a1
            delta2 = d3.T @ a2
            delta3 = d4.T @ a3
        
            delta1 /= m
            delta2 /= m
            delta3 /= m
        
            # Regularización de los gradientes
            delta1 += (lambda_ / m) * theta1
            delta2 += (lambda_ / m) * theta2
            delta3 += (lambda_ / m) * theta3
            delta3 = delta3.to_numpy()
        
            gradiente = np.concatenate((delta1.ravel(order='F'), delta2.ravel(order='F'), delta3.ravel(order='F')))
            return gradiente
      '''
    print(string)


def fmin1():
    string = '''
        maxiter = 200
        nn_params = opt.fmin_cg(maxiter=maxiter, f=nnCostFunctionReg, x0=nn_params, fprime=nnGradFunctionReg, args=(
        input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_train, y_train.flatten(), lambda_param))

      '''
    print(string)


def unroll1():
    string = '''
        inicio = 0
        fin = hidden_layer_size1 * (input_layer_size + 1)
        theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size + 1), order='F')
        inicio = fin
        fin = fin + (hidden_layer_size2 * (hidden_layer_size1 + 1))
        theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1 + 1), order='F')
        inicio = fin
        theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2 + 1), order='F')

        print('Theta1: \n', theta1)
        print('Theta2: \n', theta2)
        print('Theta3: \n', theta3)
      '''

    print(string)


def pred1():
    string = '''
        # Main
        X_test_normal = []
        for i in range(X_test.shape[0]):
          x = X_test[i] - mean
          x = x / std
          X_test_normal.append(x)

        pred = predict(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X_test_normal)
        print("Accuracy del conjunto de test: ", np.mean(pred.flatten() == y_test.flatten()) * 100)

        # Funcion
        def predict(nn_params, input_layer_size, hidden_layer_size1, hidden_layer_size2, num_labels, X):
            inicio = 0
            fin = hidden_layer_size1 * (input_layer_size + 1)
            theta1 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size1, input_layer_size + 1), order='F')
            inicio = fin
            fin = fin + (hidden_layer_size2 * (hidden_layer_size1 + 1))
            theta2 = np.reshape(a=nn_params[inicio:fin], newshape=(hidden_layer_size2, hidden_layer_size1 + 1), order='F')
            inicio = fin
            theta3 = np.reshape(a=nn_params[inicio:], newshape=(num_labels, hidden_layer_size2 + 1), order='F')

            a1, a2, a3, a4 = forward(theta1, theta2, theta3, X)

            return np.argmax(a4, axis=1)
      '''
    print(string)

def nnsk1():
    string = '''
        # Cargar los datos
        data = pd.read_csv("drivers_behavior.csv")
        y = pd.DataFrame(data['Target'])
        X = data.drop(['Target'], axis=1)
    
        # Definición parámetros RED NEURONAL
        capa_entrada = 60
        capa_oculta1 = 50
        capa_oculta2 = 25
        n_salidas = 4
    
        # Ejercicio 1: Holdout
        X_train, X_test, y_train, y_test = nn.train_test_split(X, y, train_size=0.75, random_state=42)
        print(f"X_train: {X_train}, \nX_test: {X_test}, \ny_train: {y_train}, \ny_test: {y_test}")
    
        # Ejercicio 2: Normalización
        X_train_estandarizada = sk.preprocessing.normalize(X)
        print(f"X_train_estandarizada: {X_train_estandarizada}")
    
        # Ejercicio 3: Inicialización de los pesos
        # Llamada a la función randInitializeWeights del script funcionesUtiles
        Theta1 = randInitializeWeights(capa_entrada + 1, capa_oculta1)
        Theta2 = randInitializeWeights(capa_oculta1 + 1, capa_oculta2)
        Theta3 = randInitializeWeights(capa_oculta2 + 1, n_salidas)
        nn_params = np.hstack((np.ravel(Theta1, order='F'), np.ravel(Theta2, order='F'), np.ravel(Theta3, order='F')))
    
        # Ejercicio 4: Función Forward
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        # Crea el modelo de red neuronal
        mlp = MLPClassifier(hidden_layer_sizes=(capa_oculta1, capa_oculta2), activation='logistic', max_iter=200)
        # Entrena el modelo
        mlp.fit(X_train_scaled, y_train)
    
        # Ejercicio 5: Predicción
        X_test_scaled = scaler.transform(X_test)
        predictions = mlp.predict(X_test_scaled)
        print(f"Prediccion: {predictions}")
        precision = sk.metrics.accuracy_score(y_test, y_pred=predictions)
        print(f"Precision: {precision}")
    '''
    print(string)

def carga2():
    string = '''
        print('Loading movie ratings dataset.')
    
        movies = sio.loadmat("ex8_movies.mat")
        Y = movies['Y'] # [n_items, n_users] puntuaciones de 1-5
        R = movies['R'] # [n_items, n_users] R(i,j)=1 si usuario j puntuó pelicula i
        print("Y shape", Y.shape)
        print("R shape", R.shape)
        print('\tAverage rating for the first movie (Toy Story): ', Y[0, np.where(R[0, :] == 1)[0]].mean(), "/5\n")

        #  Cargar parámetros preentrenados (X, Theta, num_users, num_movies, num_features)
        params_data = sio.loadmat('ex8_movieParams.mat')
        X = params_data['X']
        Theta = params_data['Theta']
        Theta = Theta.T #RECORDAR TRANSPONER
        print("Shape de X: ", X.shape)  # [n_items, features]
        print("Shape de Theta: ", Theta.shape)  # [features, n_users]
        
        #CARGA POR TXT EN VEZ DE MAT
        
        # Títulos de las películas en el mismo orden que las matrices Y y R
        movie_idx = {}
        f = open('movie_ids.txt', encoding='ISO-8859-1')
        for line in f:
            tokens = line.split(' ')
            tokens[-1] = tokens[-1][:-1]
            movie_idx[int(tokens[0]) - 1] = ' '.join(tokens[1:])
    
        print("Títulos de las películas en el mismo orden que las matrices Y y R. Se muestran 10 del principio.")
        for i in range(10):
            print('{0} - Nombre: {1}.'.format(str(i), movie_idx[i]))
      '''
    print(string)


def rank2():
    string = '''
        # Main
        ranking(Y, R, movie_idx, 5)
        # Funcion
        def ranking(Y, R, movies_idx, num_peliculas):
            n_movies = Y.shape[0]
            peliculas = list()
            num_valoraciones = list()
            peliculas_recomendadas = list()
        
            for i in range(n_movies):
                peliculas.append(np.where(R[i, :] == 1)[0])
                num_valoraciones.append(len(peliculas[i]))
                peliculas_recomendadas.append(np.mean(Y[i, peliculas[i]]))
        
            indices_ordenados_valoracion = np.argsort(num_valoraciones, axis=0)[::-1]
            indices_ordenados_media = np.argsort(peliculas_recomendadas, axis=0)[::-1]
        
            print(f"Primeras {num_peliculas} películas mejor valoradas (Ordenadas por valoración):")
            for i in range(num_peliculas):
                print(f"{i} Nº {indices_ordenados_valoracion[i]} con {peliculas_recomendadas[indices_ordenados_valoracion[i]]} puntos valorada {num_valoraciones[indices_ordenados_valoracion[i]]} ({movies_idx[indices_ordenados_valoracion[i]]})")
        
            print(f"Primeras {num_peliculas} peliculas mejor valoradas (Ordenadas por media):")
            for i in range(num_peliculas):
                print(
                    f"{i} Nº {indices_ordenados_media[i]} con {peliculas_recomendadas[indices_ordenados_media[i]]} puntos valorada {num_valoraciones[indices_ordenados_media[i]]} ({movies_idx[indices_ordenados_media[i]]})")
      '''
    print(string)


def cost2():
    string = '''
        # Main
        lambda_param = 0
        sub_users = 4
        sub_movies = 5
        sub_features = 3
    
        Theta = np.zeros((features, n_users))
    
        X_sub = X[:sub_movies, :sub_features]
        Theta_sub = Theta[:sub_features, :sub_users]
        Y_sub = Y[:sub_movies, :sub_users]
        R_sub = R[:sub_movies, :sub_users]
    
        params = np.hstack((np.ravel(X_sub, order='F'), np.ravel(Theta_sub, order='F')))
    
        coste_sub = cobaCostFuncReg(params, Y_sub, R_sub, sub_features, lambda_param)
        print("Coste:", coste_sub)
    
        # Funcion
        def cobaCostFuncReg(params, Y, R, num_features, lambda_param):
            n_movies = Y.shape[0]
            n_users = Y.shape[1]
        
            X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
            Theta = np.reshape(params[n_movies * num_features:], (num_features, n_users), 'F')
        
            error = np.multiply(np.dot(X, Theta) - Y, R)
            error_cuadratico = np.power(error, 2)
            J_sin_Reg = (1/2) * np.sum(error_cuadratico)
        
            J_con_reg = J_sin_Reg + ((lambda_param/2) * np.sum(np.power(X, 2))) + ((lambda_param/2) * np.sum(np.power(Theta, 2)))
        
            return J_con_reg

      '''
    print(string)


def grad2():
    string = '''
        # Main
        gradiente_sub = cobaGradientFuncReg(params, Y_sub, R_sub, sub_features, lambda_param)
            print("Gradiente:", gradiente_sub)
        # Funcion
        def cobaGradientFuncReg(params, Y, R, num_features, lambda_param):
            n_movies = Y.shape[0]
            n_user = Y.shape[1]
        
            X = np.reshape(params[:n_movies * num_features], (n_movies, num_features), 'F')
            Theta = np.reshape(params[n_movies * num_features:], (num_features, n_user), 'F')
        
            error = np.multiply(np.dot(X, Theta) - Y, R)
            Theta_grad = np.dot(X.T, error) + (lambda_param * Theta)
            X_grad = np.dot(error, Theta.T) + (lambda_param * X)
        
            grad = np.hstack((np.ravel(X_grad, order='F'), np.ravel(Theta_grad, order='F')))
        
            return grad
      '''
    print(string)


def fmin2():
    string = '''
        lambda_param = 1.5
        maxiter = 200
        X_rand = np.random.rand(n_movies, features) * (2 * 0.12)
        Theta_rand = np.random.rand(features, n_users) * (2 * 0.12)
        params = np.hstack((np.ravel(X_rand, order='F'), np.ravel(Theta_rand, order='F')))
    
        fmin = opt.fmin_cg(maxiter=maxiter, f=cobaCostFuncReg, x0=params, fprime=cobaGradientFuncReg, args=(Y, R, features, lambda_param))
    
        X = np.reshape(fmin[:n_movies * features], (n_movies, features), 'F')
        Theta = np.reshape(fmin[n_movies * features:], (features, n_users), 'F')
      '''
    print(string)


def recom2():
    string = '''
        # Main
        usuario = 2
            num_peliculas = 5
            recomendacionUsuario(X, Theta, Y, R, usuario, num_peliculas, movie_idx)
        # Funcion
        def recomendacionUsuario(X, Theta, Y, R, usuario, num_peliculas, movie_idx):
            prediccion = np.dot(X, Theta)
            n_movies = Y.shape[0]
            pelicula_recomendada = list()
        
            for i in range(n_movies):
                pelicula_recomendada.append(np.where(R[i, usuario] == 0, prediccion[i, usuario], 0))
        
            print(pelicula_recomendada)
        
            indices_pelicula_recomendada = np.argsort(pelicula_recomendada, axis=0)[::-1]
        
            print(f"Las mejores {num_peliculas} recomendaciones para el usuario {usuario}:")
            for i in range(num_peliculas):
                print(f"Tasa de predicción {pelicula_recomendada[indices_pelicula_recomendada[i]]} para la pelicula {movie_idx[indices_pelicula_recomendada[i]]}")
      '''
    print(string)


def simi2():
    string = '''
        # Main
        pelicula = 0
            similares(X, pelicula, num_peliculas)
        # Funcion
        def similares(X, pelicula, num_peliculas):
            datos_pelicula = X[pelicula]
            X = np.delete(X, pelicula, axis=0)
            distancia = np.linalg.norm(X - datos_pelicula, axis=0)
            indices_ordenados = np.argsort(distancia, axis=0)[::-1]
        
            print(f"{num_peliculas} películas parecidas a la nº {pelicula}, titulada {movie_idx[pelicula]}")
            for i in range(num_peliculas):
                print(f"Película nº {indices_ordenados[i]}, titulada {movie_idx[indices_ordenados[i]]}")
      '''
    print(string)


def km2():
    string = '''
        K = 3
        max_iters = 200
        centroids = kMeansInitCentroids(X, K)
        centroids, idx = runKmeans(X, centroids, max_iters, True)
      '''
    print(string)

def ejeEB():
    string = '''
        movies = sio.loadmat("ex8_movies.mat")
        Y = movies['Y']
        R = movies['R']
        n_items = Y.shape[0]
        n_users  = Y.shape[1]
        print("Número de películas: ", Y.shape[0], " número de usuarios: ", Y.shape[1])
        #print("Número de películas: ", R.shape[0], " número de usuarios: ", R.shape[1]) # Sería lo mismo que la sentencia anterior

        print("\nY contiene las puntuaciones/valoraciones de 1-5 de las n_i películas y los n_u usuarios.")
        print("\t Y es un ", type(Y), " con dimensiones: ", Y.shape)
        print("\nR indica si existe o no valoración de un usuario para una película.")
        print("\t R es un ", type(R), " con dimensiones: ", R.shape)

        print('\nMedia de las valoraciones de la primera película(Toy Story): ', Y[0, np.where(R[0, :] == 1)[0]].mean(), "/5\n")

        ###

        params_data = sio.loadmat("ex8_movieParams.mat")
        X = params_data['X']
        Theta = params_data['Theta']
        Theta = Theta.T
        features = X.shape[1] # Sería lo mismo que Theta.shape[0]
        print("****    *****\n\nEl número de características de los ítems (películas) es : ", features)
    
        print("\nX contiene las características preentrenadas basadas en el contenido de las películas.")
        print("\t X es un ", type(X), " con dimensiones: ", X.shape)
        print("\nTheta contiene los parámetros preentrenados de preferencia de nuestros usuarios.")
        print("\t Theta es un ", type(Theta), " con dimensiones: ", Theta.shape)
        
        def cofiCostFuncReg(params, Y, R, features, lambda_param):
            # Variables importantes
            num_movies = Y.shape[0]
            num_users = Y.shape[1]

            # Enrollar
            X = np.reshape(params[: num_movies * features], (num_movies, features), 'F')
            Theta = np.reshape(params[num_movies * features:], (features, num_users), 'F')

            # Función Coste
            error = np.multiply(np.dot(X, Theta) - Y, R)
            squared_error = np.power(error, 2)
            J_sinreg = (1. / 2) * np.sum(squared_error)

            # Añadimos regularización
            J_conreg = J_sinreg + ((lambda_param /2) * np.sum(np.power(Theta,2))) + ((lambda_param / 2) * np.sum(np.power(X, 2)))

            return J_conreg
            
            lambda_param = 1.5

            # Subconjunto de datos
            sub_users = 4
            sub_movies = 5
            sub_features = 3

            X_sub = X[:sub_movies, :sub_features]
            Theta_sub = Theta[:sub_features, :sub_users]
            Y_sub = Y[:sub_movies, :sub_users]
            R_sub = R[:sub_movies, :sub_users]

            params_sub = np.hstack((np.ravel(X_sub, order='F'), np.ravel(Theta_sub, order='F')))

            J_reg_sub = cofiCostFuncReg(params_sub, Y_sub, R_sub, sub_features, lambda_param)
            print("\nPara el subconjunto seleccionado J_reg debe ser cercano a 31.34: ",J_reg_sub)

            # Todos los datos
            params = np.hstack((np.ravel(X, order='F'), np.ravel(Theta, order='F')))
            J_reg = cofiCostFuncReg(params, Y, R, features, lambda_param)
            print("\nPara todos los datos J_reg debe ser cercano a 34821.70: ",J_reg)
            
        def cofiGradientFuncReg(params, Y, R, features, lambda_param):
            # Variables importantes
            num_movies = Y.shape[0]
            num_users = Y.shape[1]

            # Enrollar
            X = np.reshape(params[0: num_movies * features], (num_movies, features), 'F')
            Theta = np.reshape(params[num_movies * features:], (features, num_users), 'F')

            X_grad = np.zeros(X.shape) # No es necesario
            Theta_grad = np.zeros(Theta.shape) # No es necesario

            # Función Coste
            error = np.multiply(np.dot(X, Theta) - Y, R)
            Theta_grad = np.dot(X.T, error) + (lambda_param * Theta)
            X_grad = np.dot(error, Theta.T) + (lambda_param * X)
            # COMPROBAR LAS DIMENSIONES PARA PODER MULTIPLICAR O NO

            # Desenrollar
            grad = np.hstack((np.ravel(X_grad, 'F'), np.ravel(Theta_grad, 'F')))

            return grad
            
            lambda_param = 1.5

            # Subconjunto de datos
            sub_users = 4
            sub_movies = 5
            sub_features = 3

            X_sub = X[:sub_movies, :sub_features]
            Theta_sub = Theta[:sub_features, :sub_users]
            Y_sub = Y[:sub_movies, :sub_users]
            R_sub = R[:sub_movies, :sub_users]

            params_sub = np.hstack((np.ravel(X_sub, order='F'), np.ravel(Theta_sub, order='F')))

            grad_reg_sub = cofiGradientFuncReg(params_sub, Y_sub, R_sub, sub_features, lambda_param)
            print("\nGradiente para el subconjunto seleccionado: ",grad_reg_sub)

            # Todos los datos
            params = np.hstack((np.ravel(X, order='F'), np.ravel(Theta, order='F')))
            grad_reg = cofiGradientFuncReg(params, Y, R, features, lambda_param)
            print("\nGradiente para todos los datos: ",grad_reg)
            
            # Añadir nuevo usuario del que no conocemos ninguna valoración
            null_array = np.empty([n_items, 1])
            Y = np.append(Y, null_array, axis=1) # Append siempre añade al final del array. Axis=1 para añadir los valores como columna

            zeros_rating = np.zeros((n_items, 1))
            R = np.append(R, zeros_rating, axis=1) # Append siempre añade al final del array. Axis=1 para añadir los valores como columna

            n_users = n_users+1 # IMPORTANTE!
            # Inicializar Theta y X con valores random pequeños
            X = np.random.rand(n_items, features) * (2 * 0.12)
            Theta = np.random.rand(features, n_users) * (2 * 0.12)
            
        def normalizacion (n_items, n_users, R, Y):
            # Inicialización con ceros de Ymean y Ynorm con dimensiones adecuadas
            Ymean = np.zeros(( n_items,1 ))
            Ynorm = np.zeros(( n_items, n_users ))
            # Para cada ítem
            for i in range(n_items):
                idx = np.where(R[i, :] == 1)[0]
                Ymean[i] = Y[i, idx].mean()
                Ynorm[i, idx] = Y[i, idx] - Ymean[i]
            print("Mean Y matrix normalized: ", Ynorm.mean())
            return Ymean, Ynorm
            
            # Normalización con usuario nuevo
            Ymean, Ynorm = normalizacion(n_items, n_users, R, Y)
            
            
            # Desenrollar
            lambda_param = 0.1
            params_rnd = np.hstack((np.ravel(X, order='F'), np.ravel(Theta, order='F')))

            # Función optimizadora
            fmin = opt.fmin_cg(maxiter=200,f=cofiCostFuncReg, x0=params_rnd, fprime=cofiGradientFuncReg, args=(Ynorm, R, features, lambda_param))

            # Enrollar los parámetros optimizados
            X = np.reshape(fmin[:n_items * features],(n_items, features), order='F')
            Theta = np.reshape(fmin[n_items * features:],(features, n_users), order='F')
            
            predictions = np.dot(X, Theta) + Ymean # Predicciones con normalización

            my_preds = predictions[:, -1]  # Me quedo solo con el último usuario: el que he añadido nuevo
            
            # Leemos el fichero con los ids y nombres de las películas
            movie_idx = {}
            f = open('movie_ids.txt',encoding = 'ISO-8859-1')
            for line in f:
                tokens = line.split(' ')
                tokens[-1] = tokens[-1][:-1]
                movie_idx[int(tokens[0]) - 1] = ' '.join(tokens[1:])
            
            idx = np.argsort(my_preds, axis=0)[::-1] # Ordenar por las predicciones de menor a mayor y coger sus índice. [::-1] significa que le damos la vuelta a la salida: de mayor a menor

            print("Top 10 movie predictions:")
            # Imprimir las 10 películas con predicción de valoración del nuevo usuario más altas
            for i in range(10):
                j = int(idx[i])
                print('Predicted rating of {0} for movie {1}.'.format(str(float(my_preds[j])), movie_idx[j]))
            
            
    '''
    print(string)

def funcionesEPD():
    string = '''
        def cofiCostFuncSinReg(params, Y, R, caracteristicas):
            peliculas = Y.shape[0]
            usuarios = Y.shape[1]
            X = np.reshape(params[0:peliculas*caracteristicas], newshape=(peliculas, caracteristicas), order='F')
            Theta = np.reshape(params[peliculas*caracteristicas:], newshape=(caracteristicas, usuarios), order='F')
            error = np.dot(X, Theta) - Y
            error_calificadas = np.multiply(error, R)
            elevado = np.power(error_calificadas, 2)
            return (1/2) * np.sum(elevado)
        
        def cofiGradientFuncSinReg(params, Y, R, caracteristicas):
            peliculas = Y.shape[0]
            usuarios = Y.shape[1]
            X = np.reshape(params[0:peliculas * caracteristicas], newshape=(peliculas, caracteristicas), order='F')
            Theta = np.reshape(params[peliculas * caracteristicas:], newshape=(caracteristicas, usuarios), order='F')
            error = np.dot(X, Theta) - Y
            error_calificadas = np.multiply(error, R)
            #HASTA AHORA ES IGUAL QUE EL COSTE SIN REGULARIZACIÓN
            Theta_grad = np.dot(X.T, error_calificadas)
            X_grad =  np.dot(error_calificadas, Theta.T)
            grad = np.hstack((np.ravel(X_grad, order='F'), np.ravel(Theta_grad, order='F')))
            return grad
        
        def cofiCostFuncReg(params, Y, R, caracteristicas, lambda_param):
            peliculas = Y.shape[0]
            usuarios = Y.shape[1]
            X = np.reshape(params[0:peliculas * caracteristicas], newshape=(peliculas, caracteristicas), order='F')
            Theta = np.reshape(params[peliculas * caracteristicas:], newshape=(caracteristicas, usuarios), order='F')
            error = np.dot(X, Theta) - Y
            error_calificadas = np.multiply(error, R)
            elevado = np.power(error_calificadas, 2)
            J = (1 / 2) * np.sum(elevado)
            J += (lambda_param/2)* np.sum(np.power(Theta,2))
            J += (lambda_param / 2) * np.sum(np.power(X, 2))
            return J
        
        def cofiGradientFuncReg(params, Y, R, caracteristicas, lambda_param):
            peliculas = Y.shape[0]
            usuarios = Y.shape[1]
            X = np.reshape(params[0:peliculas * caracteristicas], newshape=(peliculas, caracteristicas), order='F')
            Theta = np.reshape(params[peliculas * caracteristicas:], newshape=(caracteristicas, usuarios), order='F')
            error = np.dot(X, Theta) - Y
            error_calificadas = np.multiply(error, R)
            #HASTA AHORA ES IGUAL QUE EL COSTE SIN REGULARIZACIÓN
            Theta_grad = np.dot(X.T, error_calificadas) + (lambda_param*Theta) #IMPORTANTE QUE EL REGULARIZAZO ES AÑADIENDO AL FINAL ESE MAS
            X_grad =  np.dot(error_calificadas, Theta.T) + (lambda_param*X)
            grad = np.hstack((np.ravel(X_grad, order='F'), np.ravel(Theta_grad, order='F')))
            return grad
            
            def checkNNGradients(lambda_param):
            #Create small problem
            X_t = np.random.rand(4, 3)
            Theta_t = np.random.rand(5, 3)
        
            #Zap out most entries
            Y = X_t @ Theta_t.T
            dim = Y.shape
            aux = np.random.rand(*dim)
            Y[aux > 0.5] = 0
            R = np.zeros((Y.shape))
            R[Y != 0] = 1
        
            #Run Gradient Checking
            dim_X_t = X_t.shape
            dim_Theta_t = Theta_t.shape
            X = np.random.randn(*dim_X_t)
            Theta = np.random.randn(*dim_Theta_t)
            num_users = Y.shape[1]
            num_movies = Y.shape[0]
            num_features = Theta_t.shape[1]
        
            params = np.concatenate((np.ravel(X,order='F'), np.ravel(Theta,order='F')))
        
            # Calculo gradiente mediante aproximación numérica
            mygrad = computeNumericalGradient(X, Theta, Y, R, num_features,lambda_param)
        
            #Calculo gradiente
            grad = cofiGradientFuncReg(params, Y, R, num_features,lambda_param)
        
            # Visually examine the two gradient computations.  The two columns
            # you get should be very similar.
            df = pd.DataFrame(mygrad,grad)
            print(df)
        
            # Evaluate the norm of the difference between two solutions.
            # If you have a correct implementation, and assuming you used EPSILON = 0.0001
            # in computeNumericalGradient.m, then diff below should be less than 1e-9
            diff = np.linalg.norm((mygrad-grad))/np.linalg.norm((mygrad+grad))
        
            print('If your gradient implementation is correct, then the differences will be small (less than 1e-9):' , diff)
        
        
        def computeNumericalGradient(X,Theta, Y, R, num_features,lambda_param):
            mygrad = np.zeros(Theta.size + X.size)
            perturb = np.zeros(Theta.size + X.size)
            myeps = 0.0001
            params = np.concatenate((np.ravel(X, order='F'), np.ravel(Theta, order='F')))
        
            for i in range(np.size(Theta)+np.size(X)):
                # Set perturbation vector
                perturb[i] = myeps
                params_plus = params + perturb
                params_minus = params - perturb
                cost_high = cofiCostFuncReg(params_plus, Y, R, num_features,lambda_param)
                cost_low = cofiCostFuncReg(params_minus, Y, R, num_features,lambda_param)
        
                # Compute Numerical Gradient
                mygrad[i] = (cost_high - cost_low) / float(2 * myeps)
                perturb[i] = 0
        
            return mygrad
    '''
    print(string)


def pasos3():
    print("1 - Carga de datos\n"
          "2 - Find closets centroids\n"
          "3 - Compute centroids\n"
          "4 - Kmeans\n"
          "5 - Ini centroids random\n"
          "6 - Elbow\n"
          "7 - Completo con cohesion y separacion\n")

def carga3():
    string = '''
        X = sio.loadmat("ex7data2.mat")['X']
        print(X.shape)
        for i in range(len(X)):
            plt.scatter(X[i][0], X[i][1], color="blue")
        plt.show()
    '''
    print(string)

def fcc3():
    string = '''
        #Main
        K = 3  # 3 Centroids
        initial_centroids = np.array([[3.0, 3.0], [6.0, 2.0], [8.0, 5.0]])
        print("Finding closest centroids\n")
        idx = findClosestCentroids(X, initial_centroids)
        print("Closest centroids for the first 3 examples: ", idx[0:3])
        
        # Funcion
        def findClosestCentroidsF(X, centroids):
            K = centroids.shape[0]
            cluster = []
            for data in X:
                eucl_dist = []
                for k in range(K):
                    eucl_dist.append(np.linalg.norm(data - centroids[k]))
                    #eucl_dist.append(np.sqrt(np.sum(np.abs(data - centroids[k])**2))
                cluster.append(np.argmin(eucl_dist))
            return np.asarray(cluster)
    '''
    print(string)

def compc3():
    string = '''
            # Main
            centroids = computeCentroids(X, idx, K)
            
            # Funcion
            def computeCentroids(X, idx, K):
                centroids = []
                for k in  range(K):
                    arr_aux = []
                    for j in  range(len(X)):
                        if idx[j] == k:
                            arr_aux.append(X[j])
                    media_centroids = np.mean(arr_aux, axis=0)
                    centroids.append(media_centroids)
                return np.asarray(centroids)
    '''
    print(string)


def kmean3():
    string = '''
            # Main
            max_iters = 10
            centroids, idx = runKmeans(X, initial_centroids, max_iters, plot=True)
            
            # Funcion
            def runKmeans(X, initial_centroids, max_iters, plot=True):
                K = len(initial_centroids)
                antiguos_centroides = initial_centroids
                for i in range(max_iters):
                    idx = findClosestCentroids(X, initial_centroids)
                    initial_centroids = computeCentroids(X, idx, K)
                if plot==True:
                    plotClusters(X, idx, initial_centroids,antiguos_centroides)
                return initial_centroids, idx
                '''
    print(string)


def randini3():
    string = '''
            # Main
            random_initial_centroids = kMeansInitCentroids(X, K)
            centroids, idx = runKmeans(X, random_initial_centroids, max_iters, plot=True)
            
            # Funcion
            def kMeansInitCentroids(X, K):
                m, n = X.shape
                np.random.seed(11)
                indices_filas = np.random.randint(0, m, K)
                centroids = np.zeros((K, n))
                for k in range(K):
                    centroids [k] = X[indices_filas[k]]
                return centroids
    '''
    print(string)

def elbow3():
    string = '''
            # Main
            elbowMethod(X)
            
            # Funcion
            def elbowMethod(X):
                costes = []
            
                for K in range(1,11):
                    coste = 0
                    initial_centroids = kMeansInitCentroids(X, K)
                    centroids, indice_centroid = runKmeans(X, initial_centroids, max_iters=10, plot=False)
            
                    # h es cada elemento de X
                    for j in range(len(X)):
                        coste += np.sum(np.power((X[j] - centroids[indice_centroid[j]]), 2))
                    costes.append(coste)
            
                num_clusters = [i for i in range(1,11)]
                plt.plot(num_clusters, costes)
                plt.show()
    '''
    print(string)

def clustsk3():
    string = '''
            # Main
            X, _ = make_blobs(n_samples=200, centers=4, random_state=0)
            inertias = []
        
            # Determinar el número óptimo de clusters
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, init='k-means++')
                kmeans.fit(X)
        
            inertias.append(kmeans.inertia_)
        
            plt.plot(range(1, 11), inertias, marker='o')
            plt.xlabel('Número de Clusters (K)')
            plt.ylabel('Inercia')
            plt.title('Método del Codo')
            plt.show()
        
            kneedle = KneeLocator(range(1, 11), inertias, curve='convex', direction='decreasing')
            optimal_k = kneedle.knee
        
            print("Número óptimo de clusters (k):", optimal_k)
        '''
    print(string)

def coheSepara():
    string = '''
        #MAIN
        K = 3  # 3 Centroids
        initial_centroids = np.array([[1.0, 5.0], [3.0, 5.5], [3.0, 1.0]])
    
        ## EXAMEN:
    
        ## 1. Crear funciones cohesion(X, centroids, idx) y separacion(centroids)
    
        max_iters = 10
    
        centroids, idx = runKmeans(X, initial_centroids, max_iters, plot=True)
    
        co = cohesion(X, centroids, idx)
    
        se = separacion(centroids)
    
        print("Cohesion:", co, "\nSeparacion: ", se)
    
    
        ## 2. Realizar la función runKmeansSin(X, initial_centroids, plot=False, lim=0.1) con un criterio de parada nuevo (lim)
        centroids, idx, i = runKmeansSin(X, initial_centroids, plot=True, lim=0.1)
    
        co = cohesion(X, centroids, idx)
    
        se = separacion(centroids)
    
        print("\n\nCohesion:", co, "\nSeparacion: ", se, "\nIteraciones: ", i)
    
        initial_centroids = kMeansInitFarCentroids(X, 3)
    
        centroids, idx, i = runKmeansSin(X, initial_centroids, plot=True, lim=0.1)
    
        co = cohesion(X, centroids, idx)
    
        se = separacion(centroids)
    
        print("\n\nCohesion:", co, "\nSeparacion: ", se, "\nIteraciones: ", i)
        
        #FUNCION
    def cohesion(X, centroids, idx):
        suma = 0
        for i in range(X.shape[0]):
            suma += np.linalg.norm(X[i] - centroids[idx[i]])
        return suma

    def separacion(centroids):
        suma = 0
        for i in range(centroids.shape[0]):
            for j in range(i, centroids.shape[0]):
                suma += np.linalg.norm(centroids[i] - centroids[j])
        return suma
    
    def getDistance(ant_centroids, centroids):
        suma = 0
        for i in range(centroids.shape[0]):
            suma += np.linalg.norm(centroids[i] - ant_centroids[i])
        return suma


    def runKmeansSin(X, initial_centroids, plot=False, lim=0.1):
        K = initial_centroids.shape[0]
        centroids = initial_centroids
        idx = np.zeros(X.shape[0])

        dif = lim + 1

        i = 0

        while dif > lim:
            ant_centroids = centroids
            # Busco los centroides mas cercanos de cada dato
            idx = findClosestCentroids(X, centroids)
            # Actualizo los centroides segun los datos que pertenezcan a el
            centroids = computeCentroids(X, idx, K)
            dif = getDistance(ant_centroids, centroids)
            i += 1

        if plot:
            plotClusters(X, idx, centroids, initial_centroids)

        return centroids, idx, i
        
        
        def kMeansInitFarCentroids(X, K):
    
        c1 = X[np.random.randint(0, X.shape[0])]
    
        centroids = [c1]
    
        for i in range(1, K):
            dist = 0
            val = 0
            for j in range(X.shape[0]):
                dist2 = 0
                for k in range(len(centroids)):
                    dist2 += np.linalg.norm(centroids[k] - X[j])
                if dist < dist2:
                    dist = dist2
                    val = j
            centroids.append(X[val])
    
        return np.asarray(centroids)
    
    def plotClusters(X, clusters, centroids, ini_centroids):
        # Assigning specific color to each cluster. Assuming 5 for now
        cols = {0: 'b', 1: 'g', 2: 'coral', 3: 'c', 4: 'lime'}
        fig, ax = plt.subplots()

        # Plots every cluster points
        for i in range(len(clusters)):
            ax.scatter(X[i][0], X[i][1], color=cols[clusters[i]], marker="+")

        # Plots all the centroids and mark them with a circle around
        for j in range(len(centroids)):
            # Plot current centroids with circle
            ax.scatter(centroids[j][0], centroids[j][1], color=cols[j])
            ax.add_artist(plt.Circle((centroids[j][0], centroids[j][1]), 0.4, linewidth=2, fill=False))
            # Plot initial centroids with ^ and circle in yellow
            ax.scatter(ini_centroids[j][0], ini_centroids[j][1], marker="^", s=150, color=cols[j])
            ax.add_artist(plt.Circle((ini_centroids[j][0], ini_centroids[j][1]), 0.4, linewidth=2, color='y', fill=False))

        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        ax.set_title("K-means Clustering")
        plt.show()
    
    '''
    print(string)

def rlineal4():
    string = '''
        def costFunction(data_x, data_y, theta):
            m = len(data_x)
            h = hipothesis(data_x, theta)
            return np.sum((h - data_y)**2)/(2*m)
        
        def hipothesis(data_x, theta):
            return data_x @ theta
        
        def gradientFunction(data_x, data_y, theta):
            m = len(data_x)
            h = hipothesis(data_x, theta)
            return np.dot(data_x.T, h - data_y) / m
        
        def gradient_descent_method(data_x, data_y, theta, alpha=0.01, iterations=1500):
            theta_opt = theta
            for _ in range(iterations):
                theta_opt = theta_opt - alpha * gradientFunction(data_x, data_y, theta_opt)
            return theta_opt
        
        if _name_ == "_main_":
            filename = "ex1data1.csv"
            dataframe = pd.read_csv(filename)
            m = len(dataframe)
            data_x = np.hstack(
                (np.ones(shape=(m, 1)),
                 dataframe.iloc[:, :-1].to_numpy())
            )
            data_y = dataframe.iloc[:, -1:].to_numpy()
        
            theta = np.zeros(shape=(data_x.shape[1], 1))
        
            print(costFunction(data_x, data_y, theta))
        
            plt.scatter(dataframe["population"], dataframe["profit"], marker='x', c='red')
            theta_opt = gradient_descent_method(data_x, data_y, theta)
        
            def prediction(x):
                return theta_opt[0] + theta_opt[1] * x
        
            plt.plot(dataframe["population"], dataframe["population"].map(prediction))
            plt.show()
            print(costFunction(data_x, data_y, theta_opt))
        '''
    print(string)

def rlogi4():
    string = '''
        def nomalizacionEstandarizada(X):
            mu = np.mean(X,axis=0)
            sigma = np.std(X, axis=0)
            return ((X-mu)/sigma),mu,sigma
            
        def crossvalidation(X, K):
            tamfolds = round(len(X) / K)
            all_indices = []
            all_folds = []

            for i in range(K):
                print(i)
                fold = []
                while len(fold) < tamfolds:
                    indexRandom = randrange(len(X))

                    if indexRandom not in all_indices:
                        fold.append(indexRandom)
                        all_indices.append(indexRandom)
                all_folds.append(fold)

            return all_folds
            
        def sigmoid(z):
            return 1 / (1 + np.exp(-z))
        
        def hipothesis(data_x, theta):
            return sigmoid(np.dot(data_x, theta))
        
        def costFunction(data_x, data_y, theta):
            m = len(data_y)
            h = hipothesis(data_x, theta)
            return - np.sum((data_y * np.log(h)) + ((1 - data_y) * np.log(1 - h)))/m
        
        def gradientFunction(data_x, data_y, theta):
            m = len(data_y)
            h = hipothesis(data_x, theta)
            return (data_x.T @ (h - data_y)) / m
        
        def gradientDescentMethod(data_x, data_y, theta, iterations, alpha):
            theta_opt = theta
            for _ in tqdm(range(iterations)):
                theta_opt = theta_opt - alpha * gradientFunction(data_x, data_y, theta_opt)
            return theta_opt
        
        def predict(x, theta, do_round=False):
            if do_round:
                h = np.round(sigmoid(np.dot(x, theta)))
            else:
                h = sigmoid(np.dot(x, theta))
            return h
        
        if _name_ == "_main_":
            filename = input("nombre del archivo: ")
            dataframe = pd.read_csv(filename)
            m = len(dataframe)
        
            data_x = np.hstack((np.ones(shape=(m, 1)), dataframe.iloc[:, :-1].to_numpy()))
            data_y = dataframe.iloc[:, -1:].to_numpy()
            theta = np.zeros(shape=(data_x.shape[1], 1))  # Recuerda theta es un vector de 1 fila x num de cols + 1
        
            print("Coste para theta = [0,0,0]")
            print(costFunction(data_x, data_y, theta))
        
            print("Descenso del gradiente")
            theta_opt = gradientDescentMethod(data_x, data_y, theta, iterations=1_000_000, alpha=0.004)
            print(theta_opt)
        '''
    print(string)

def plot():
    string = '''
        plt.plot(range(1, 11), inertias)
        plt.title("Elbow method")
        plt.xlabel("Number of clusters")
        plt.ylabel("Inertia")
        plt.show()
        '''
    print(string)

def frontera():
    string = '''
        # Main
        ejehorizontal = [min(X['score_1']), max(X['score_2'])]
        ejevertical = - (theta_opt[0] + np.dot( ejehorizontal, theta_opt[1])) / theta_opt[2]
        plotDataFrontera(X, y, ejehorizontal, ejevertical)
        # Funcion
        def plotDataFrontera(X, y, ejehorizontal, ejevertical):
            admitted = X[y["label"] == 1]
            not_admitted = X[y["label"] == 0]
        
            plt.scatter(admitted["score_1"], admitted["score_2"], color='blue', label='Admitido', marker="x")
            plt.scatter(not_admitted["score_1"], not_admitted["score_2"], color='yellow', label='No Admitido')
            plt.plot(ejehorizontal, ejevertical , c='b')  # dibujar la frontera de decisión
            plt.legend()
            plt.xlabel('Score 1')
            plt.ylabel('Score 2')
            plt.show()
        '''
    print(string)

def seaborn():
    string = '''
        data = pd.read_csv("iris.data")
        columnas = ["sepal_length", "sepal_width", "petal_length", "petal_width", "clase"]
        data.columns = columnas
        seaborn.pairplot(data, hue="clase")
        plt.show()    
        '''
    print(string)
    
def misioneros():
    string = '''
        #MAIN
        myc = Canibal_Misionero((3,3,1))
        
        #FUNCION
    class Canibal_Misionero(Problem):
        """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
        squares is a blank. A state is represented as a tuple of length 9, where  element at
        index i represents the tile number  at index i (0 if it's an empty square) """
    
        def __init__(self, initial=(3, 3, 1), goal=(0, 0, 0)):
            """ Define goal state and initialize a problem """
            super().__init__(initial, goal)
    
        def getMisioneros(self, state):
            return state[0]
    
        def getCanibales(self, state):
            return state[1]
    
        def getBarca(self, state):
            return state[2]
    
        # Devuelve si el estado futuro es peligroso o no
        def estadoPeligroso(self, c, m):
            return (m < c and m != 0) or (m > c and m != 3)
    
        def canMoveBoat(self, state, cadena):
    
            # Para un movimiento 1-1 solo hay que comprobar que se pueda hacer, no hace falta más
            if cadena == 'M1C1':
                # Está en el lado izquierdo
                if self.getBarca(state) == 1:
                    return self.getMisioneros(state) != 0 and self.getCanibales(state) != 0
                else:
                    return 3 - self.getMisioneros(state) != 0 and 3 - self.getCanibales(state) != 0
            if cadena == 'M2C0':
                # Está en el lado izquierdo
                if self.getBarca(state) == 1:
                    # No hay que comprobar el otro lado xq lo que se va a hacer es aumentar el numero de misioneros asi que todo bien
                    return (self.getMisioneros(state) - 2 >= 0 and
                            not self.estadoPeligroso(self.getCanibales(state), self.getMisioneros(state) - 2))
                else:
                    return ((3 - self.getMisioneros(state) - 2) >= 0 and
                            not self.estadoPeligroso(3 - self.getCanibales(state), 3 - self.getMisioneros(state) - 2))
            if cadena == 'M0C2':
                # Está en el lado izquierdo
                if self.getBarca(state) == 1:
                    # Hay que comprobar lo que pasa en el otro lado, no aqui, porque aqui solo disminuye el número de notas
                    return (self.getCanibales(state) - 2 >= 0 and
                            not self.estadoPeligroso(3 - self.getCanibales(state) + 2, 3 - self.getMisioneros(state)))
    
                else:
                    return ((3 - self.getCanibales(state) - 2) >= 0 and
                            not self.estadoPeligroso(self.getCanibales(state) + 2, self.getMisioneros(state)))
            if cadena == 'M0C1':
                # Está en el lado izquierdo
                if self.getBarca(state) == 1:
                    # Hay que comprobar lo que pasa en el otro lado, no aqui, porque aqui solo disminuye el número de notas
                    return (self.getCanibales(state) - 1 >= 0 and
                            not self.estadoPeligroso(3 - self.getCanibales(state) + 1, 3 - self.getMisioneros(state)))
    
                else:
                    return ((3 - self.getCanibales(state) - 1) >= 0 and
                            not self.estadoPeligroso(self.getCanibales(state) + 1, self.getMisioneros(state)))
            if cadena == 'M1C0':
                # Está en el lado izquierdo
                if self.getBarca(state) == 1:
                    # No hay que comprobar el otro lado xq lo que se va a hacer es aumentar el numero de misioneros asi que todo bien
                    return (self.getMisioneros(state) - 1 >= 0 and
                            not self.estadoPeligroso(self.getCanibales(state), self.getMisioneros(state) - 1))
                else:
                    return ((3 - self.getMisioneros(state) - 1) >= 0 and
                            not self.estadoPeligroso(3 - self.getCanibales(state), 3 - self.getMisioneros(state) - 1))
    
            return state.index(0)
    
        def moveBoat(self, state, m, c):
            if state[2] == 1:
                state[2] = 0
            else:
                state[2] = 1
            state[0] += m
            state[1] += c
    
        def actions(self, state):
            """ Return the actions that can be executed in the given state.
            The result would be a list, since there are only four possible actions
            in any given state of the environment """
    
            possible_actions = []
            if self.canMoveBoat(state, 'M1C1'):
                possible_actions.append('M1C1')
            if self.canMoveBoat(state, 'M0C1'):
                possible_actions.append('M0C1')
            if self.canMoveBoat(state, 'M1C0'):
                possible_actions.append('M1C0')
            if self.canMoveBoat(state, 'M2C0'):
                possible_actions.append('M2C0')
            if self.canMoveBoat(state, 'M0C2'):
                possible_actions.append('M0C2')
    
            return possible_actions
    
        def result(self, state, action):
            """ Given state and action, return a new state that is the result of the action.
            Action is assumed to be a valid action in the state """
    
            new_state = list(state)
            # Aux multiplica por 1 o -1 para sumar si esta a la derecha y restar si está a la izquierda
            aux = -1
            if state[2] == 0:
                aux = 1
    
            if action == 'M1C1':
                self.moveBoat(new_state, aux, aux)
            elif action == 'M1C0':
                self.moveBoat(new_state, aux, 0)
            elif action == 'M0C1':
                self.moveBoat(new_state, 0, aux)
            elif action == 'M2C0':
                self.moveBoat(new_state, aux * 2, 0)
            elif action == 'M0C2':
                self.moveBoat(new_state, 0, aux * 2)
    
            return tuple(new_state)
    
        def goal_test(self, state):
            """ Given a state, return True if state is a goal state or False, otherwise """
            return state == self.goal
    
        def check_solvability(self, state):
            """ Checks if the given state is solvable """
    
            inversion = 0
            for i in range(len(state)):
                for j in range(i + 1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
    
            return inversion % 2 == 0
    
        def h(self, node):
            """ Return the heuristic value for a given state. Default heuristic function used is
            h(n) = number of misplaced tiles """
            return self.getMisioneros(node.state) + self.getCanibales(node.state)

    '''
    
    print(string)
    
    
def cantaros():
    string = '''
        #MAIN
        can = Cantaros((0,0), (2,0))
        #FUNCIONES
        
        class Cantaros(Problem):
        
            def __init__(self, initial, goal):
                """ Define goal state and initialize a problem """
                super().__init__(initial, goal)
        
            def get4(self, state):
                return state[0]
        
            def get3(self, state):
                return state[1]
        
            def canMove(self, state, cadena):
                """
                Movimientos posibles: UP, DOWN, LEFT, RIGHT
                """
                if cadena == 'FULL3':
                    return self.get3(state) < 3
                elif cadena == 'FULL4':
                    return self.get4(state) < 4
                elif cadena == '3EN4':
                    return self.get4(state) < 4 and self.get3(state) > 0
                elif cadena == '4EN3':
                    return self.get3(state) < 3 and self.get4(state) >0
                elif cadena == 'VACIA3':
                    return self.get3(state) > 0
                elif cadena == 'VACIA4':
                    return self.get4(state) > 0
                return state.index(0)
        
        
            def actions(self, state):
                """ Return the actions that can be executed in the given state.
                The result would be a list, since there are only four possible actions
                in any given state of the environment """
        
                possible_actions = []
                if self.canMove(state, 'FULL3'):
                    possible_actions.append('FULL3')
                if self.canMove(state, 'FULL4'):
                    possible_actions.append('FULL4')
                if self.canMove(state, '3EN4'):
                    possible_actions.append('3EN4')
                if self.canMove(state, '4EN3'):
                    possible_actions.append('4EN3')
                if self.canMove(state, 'VACIA3'):
                    possible_actions.append('VACIA3')
                if self.canMove(state, 'VACIA4'):
                    possible_actions.append('VACIA4')
        
                return possible_actions
        
            def full3(self, state):
                state[1] = 3
        
            def full4(self, state):
                state[0] = 4
        
            def pasa3a4(self, state):
                if 4 < state[1] + state[0]:
                    state[1] -= (4 - state[0])
                    state[0] = 4
                else:
                    state[0] = state[1] + state[0]
                    state[1] = 0
        
            def pasa4a3(self, state):
                if 3 < state[1] + state[0]:
                    state[0] -= 3 - state[1]
                    state[1] = 3
                else:
                    state[0] = 0
                    state[1] = state[1] + state[0]
        
            def vacia(self, state, i):
                state[i] = 0
        
            def result(self, state, action):
                """ Given state and action, return a new state that is the result of the action.
                Action is assumed to be a valid action in the state """
        
                new_state = list(state)
        
                if action == 'FULL3':
                    self.full3(new_state)
                elif action == 'FULL4':
                    self.full4(new_state)
                elif action == '3EN4':
                    self.pasa3a4(new_state)
                elif action == '4EN3':
                    self.pasa4a3(new_state)
                elif action == 'VACIA3':
                    self.vacia(new_state, 1)
                elif action == 'VACIA4':
                    self.vacia(new_state, 0)
        
                return tuple(new_state)
        
            def goal_test(self, state):
                """ Given a state, return True if state is a goal state or False, otherwise """
                return state == self.goal
        
            def check_solvability(self, state):
                """ Checks if the given state is solvable """
        
                inversion = 0
                for i in range(len(state)):
                    for j in range(i + 1, len(state)):
                        if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                            inversion += 1
        
                return inversion % 2 == 0
        
            def h(self, node):
                """ Return the heuristic value for a given state. Default heuristic function used is
                h(n) = number of misplaced tiles """
                return np.abs(self.get4(node.state) - self.goal[0]) + np.abs(self.get3(node.state) - self.goal[1])
        
    
    '''
    print(string)
    
    
def laberinto():
    string = '''
            class Laberinto(Problem):
                def __init__(self, initial, goal, matrix):
                    """ Define goal state and initialize a problem """
                    super().__init__(initial, goal)
                    self.matrix = matrix
            
                def getX(self, state):
                    return state[0]
            
                def getY(self, state):
                    return state[1]
            
                def canMove(self, state, cadena):
                    """
                    Movimientos posibles: UP, DOWN, LEFT, RIGHT
                    """
                    if cadena == 'UP':
                        return self.getX(state) - 1 > 0 and \
                               self.matrix[self.getX(state)-1][self.getY(state)] == 'O'
                    elif cadena == 'DOWN':
                        return self.getX(state) + 1 < len(self.matrix) and \
                               self.matrix[self.getX(state)+1][self.getY(state)] == 'O'
                    elif cadena == 'LEFT':
                        return self.getY(state) - 1 > 0 and \
                               self.matrix[self.getX(state)][self.getY(state)-1] == 'O'
                    elif cadena == 'RIGHT':
                        return self.getY(state) + 1 < len(self.matrix) and \
                               self.matrix[self.getX(state)][self.getY(state)+1] == 'O'
                    return state.index(0)
            
                def move(self, state, x, y):
                    state[0] += x
                    state[1] += y
            
                def actions(self, state):
                    """ Return the actions that can be executed in the given state.
                    The result would be a list, since there are only four possible actions
                    in any given state of the environment """
            
                    possible_actions = []
                    if self.canMove(state, 'UP'):
                        possible_actions.append('UP')
                    if self.canMove(state, 'DOWN'):
                        possible_actions.append('DOWN')
                    if self.canMove(state, 'LEFT'):
                        possible_actions.append('LEFT')
                    if self.canMove(state, 'RIGHT'):
                        possible_actions.append('RIGHT')
            
                    return possible_actions
            
                def result(self, state, action):
                    """ Given state and action, return a new state that is the result of the action.
                    Action is assumed to be a valid action in the state """
            
                    new_state = list(state)
            
                    if action == 'UP':
                        self.move(new_state, -1, 0)
                    elif action == 'DOWN':
                        self.move(new_state, 1, 0)
                    elif action == 'LEFT':
                        self.move(new_state, 0, -1)
                    elif action == 'RIGHT':
                        self.move(new_state, 0, 1)
            
                    return tuple(new_state)
            
                def goal_test(self, state):
                    """ Given a state, return True if state is a goal state or False, otherwise """
                    return state == self.goal
            
                def check_solvability(self, state):
                    """ Checks if the given state is solvable """
            
                    inversion = 0
                    for i in range(len(state)):
                        for j in range(i + 1, len(state)):
                            if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                                inversion += 1
            
                    return inversion % 2 == 0
            
                def h(self, node):
                    """ Return the heuristic value for a given state. Default heuristic function used is
                    h(n) = number of misplaced tiles """
                    return abs(self.goal[0] - node.state[0]) + abs(self.goal[1] - node.state[1])
    '''
    
    print(string)


def laberinto2():
    string = '''
        
        mapa = (('O', 'X', 'O', 'O', 'O', 'X', 'X', 'O', 'X', 'O'),
                ('O', 'X', 'O', 'X', 'O', 'O', 'O', 'O', 'X', 'O'),
                ('O', 'X', 'O', 'X', 'O', 'X', 'X', 'X', 'X', 'O'),
                ('O', 'X', 'O', 'X', 'X', 'X', 'O', 'O', 'O', 'O'),
                ('O', 'O', 'O', 'O', 'O', 'X', 'O', 'X', 'O', 'X'),
                ('O', 'X', 'X', 'X', 'O', 'X', 'O', 'X', 'O', 'X'),
                ('O', 'X', 'O', 'O', 'O', 'X', 'O', 'X', 'O', 'X'),
                ('O', 'X', 'O', 'X', 'X', 'X', 'O', 'X', 'O', 'X'),
                ('O', 'X', 'O', 'O', 'O', 'O', 'O', 'X', 'O', 'X'),
                ('O', 'X', 'O', 'X', 'X', 'X', 'X', 'X', 'O', 'X'))

        class Laberinto(Problem):
            """ Problema del laberinto donde un robot iría desde una posición de entrada a una de salida """
        
            def canMoveLab(self, state, where):
                retVal = True
        
                if (where == 'LEFT'):
                    retVal = ((state[1]!=0) and (mapa[state[0]][state[1]-1]!='X'))
                elif (where == 'RIGHT'):
                    retVal = ((state[1]!=9) and (mapa[state[0]][state[1]+1]!='X'))
                elif (where == 'UP'):
                    retVal = ((state[0]!=0) and (mapa[state[0]-1][state[1]]!='X'))
                elif (where == 'DOWN'):
                    retVal = ((state[0]!=9) and (mapa[state[0]+1][state[1]]!='X'))
        
                return retVal
        
            def __init__(self, initial=(4, 0), goal=(0, 9)):
                """ Define goal state and initialize a problem """
                super().__init__(initial, goal)
        
            def actions(self, state):
                """ Return the actions that can be executed in the given state.
                The result would be a list, since there are only four possible actions
                in any given state of the environment """
        
                possible_actions = []
        
                if self.canMoveLab(state,'LEFT'):
                    possible_actions.append('LEFT')
                if self.canMoveLab(state,'RIGHT'):
                    possible_actions.append('RIGHT')
                if self.canMoveLab(state,'UP'):
                    possible_actions.append('UP')
                if self.canMoveLab(state,'DOWN'):
                    possible_actions.append('DOWN')
        
                return possible_actions
        
            def result(self, state, action):
                """ Given state and action, return a new state that is the result of the action.
                Action is assumed to be a valid action in the state """
        
                new_state = list(state)
        
                if (action == 'LEFT'):
                    new_state[1] -= 1
                elif (action == 'RIGHT'):
                    new_state[1] += 1
                elif (action == 'UP'):
                    new_state[0] -= 1
                elif (action == 'DOWN'):
                    new_state[0] += 1
        
                return tuple(new_state)
        
            def goal_test(self, state):
                """ Given a state, return True if state is a goal state or False, otherwise """
        
                return state == self.goal
        
            def h(self, node):
                """ Return the heuristic value for a given state."""
        
                return abs(self.goal[0] - node.state[0]) + abs(self.goal[1] - node.state[1])
        
        # Comienzo--------
        
        if __name__ == '__main__':
            print('Laberinto.')
        
            lab = Laberinto()
        
            print(astar_search(lab).solution())
               
    '''

    print(string)
    
    