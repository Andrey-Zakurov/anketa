#******************************************************************************#
# acneta                                                                       #
#                                                                              #
#******************************************************************************#
# Andrey 2022-08-29                                                            #
#                                                                              #
#******************************************************************************#
# Приложение анкетирования, из задания Митяя                                   #
#******************************************************************************#


#
class anketa():
  '''в этом классе логика опросника с
  проверками и методами ввода вывода'''

  # метод инициализации обьекта
  def __init__(self, dict_data):
    self.questions = dict_data
    self.result = []

  # метод проверок введенного пользователем
  def _is_valid(self, key, text):
    # если проверка пройдет флаг станет тру и
    # по нему идет ретурн
    self.flag = False
    
    # проверка на слова
    if key == 'letters':
      if text.isalpha():
        self.flag = True
    # проверка на число
    if key == 'int_age':
      if text.isnumeric() and 0 < int(text) < 100:
        self.flag = True
    # пофиг что введено
    if key == 'all':
      if text:
        self.flag = True

    # ретурн блок
    if self.flag:
      return True
    else:
      return False
    
    
  # метод проводящий опрос
  def questioning(self):
    temp = ''
    # перебираем вопросы
    for question in self.questions:
      while True:
        # получаем ответ от пользователя
        temp = input(f'please enter your {question}: ')
        # проверочка
        if self._is_valid(self.questions[question], temp):
          # вопрос и ответ записываются в массив
          self.result.append((question, temp))
          break
    return True

  def output_terminal(self):
    for i in range(len(self.result)):
      print(f'You {self.result[i][0]}: {self.result[i][1]}')



# это условие True, если этот файл запускается
# а не подключается в качестве модуля
if __name__ == '__main__':

  # вопрос и ключ для метода проверки
  data = {
      'name': 'letters',
      'surname': 'letters',
      'age': 'int_age',
      'hobby': 'all'
  }

  # инициализация обьекта, с внесением вопросов с ключами в него
  Obj = anketa(data)

  # если тест окончен выводится результат в терминал
  if Obj.questioning():
    Obj.output_terminal()
  
