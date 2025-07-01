from .Types import DefaultTypes


def GetUser(obj: DefaultTypes.UpdateObject) -> DefaultTypes.User:
    """Извлечь данные пользователя из объекта обновления

    Args:
        obj (DefaultTypes.UpdateObject): Объект обновления

    Raises:
        ValueError: Не удалось определить тип объекта обновления

    Returns:
        DefaultTypes.User: Данные пользователя
    """
    
    if isinstance(obj, DefaultTypes.Message):
        return obj.from_user
    elif isinstance(obj, DefaultTypes.CallbackQuery):
        return obj.from_user
    raise ValueError()


def GetChat(obj: DefaultTypes.UpdateObject) -> DefaultTypes.Chat:
    """Извлечь данные чата из объекта обновления

    Args:
        obj (DefaultTypes.UpdateObject): Объект обновления

    Raises:
        ValueError: Не удалось определить тип объекта обновления

    Returns:
        DefaultTypes.Chat: Данные чата
    """
    if isinstance(obj, DefaultTypes.Message):
        return obj.chat
    elif isinstance(obj, DefaultTypes.CallbackQuery):
        return obj.message.chat
    raise ValueError()