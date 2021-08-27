import  wave, os 
from datetime import datetime, timedelta
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty,ABCMeta
from pyaudio import PyAudio, paInt16

class AudioRecorderContract(ABC):
    _format = None
    _buffer_size= None
    _channels= None
    _rate= None
    _stream= None
    _file= None
    _wave= None

    # _stream=None
    # _stream=None

    @abstractproperty
    def file_name(self):
        pass
    
    # @abstractproperty
    @file_name.setter
    def file_name(self, name):
        pass
    
    @abstractclassmethod
    def get_file(self):
        pass

    @abstractclassmethod
    def run(cls):
        pass
    
    @abstractmethod
    def _create_file(self):
        pass
    
    @abstractmethod
    def get_stream(self):
        pass

    @abstractmethod
    def _create_stream(self):
        pass

    @abstractmethod
    def _config_stream(self):
        pass

    @abstractmethod
    def _create_wave(self):
        pass

    @abstractmethod
    def get_wave(self):
        pass
    
    @abstractmethod
    def get_audio_handler(self):
        pass
    
    @abstractmethod
    def save_wave(self):
        pass


class AudioRecorder(AudioRecorderContract):
    duration_in_secs = 40
    file_extension = 'wav'
    buffers=[]
    file_name = 'AudioRecorder'.strip().lower()
    _channels = 2
    _buffer_size = 1024
    _format = paInt16
    _rate=44100


    def run(cls):
        cls._write_stream()
        cls.save_wave()
    
    def _create_stream(self):
        self._audio_handler = PyAudio()
    
    def _write_stream(self):
        self._create_stream()
        self._config_stream()
        
        now = self.current_time()
        end_time = now + timedelta(seconds = self.duration_in_secs)
        print('recording..')
        while now <= end_time:
            self.buffers.append(self.get_stream().read(self._buffer_size))
            now = self.current_time()


    def current_time(self):
        return datetime.now()

    def _config_stream(self):
        self._stream = self.get_audio_handler().open(
            input=True,
            rate=self._rate,
            channels=self._channels,
            format=self._format,
            frames_per_buffer= self._buffer_size
        )

    def get_stream(self):
        return self._stream

    def _create_file(self):
        if os.path.exists(self.get_file()):
            self.file_name+= '_' + self.current_time().strftime('%d-%m-%Y_%H:%I:%S')

    def get_file(self):
        return f"{self.file_name}.{self.file_extension}"

    def _create_wave(self):
        self._create_file()
        self._wave = wave.open(self.get_file(), 'wb')

    def get_wave(self):
        return self._wave

    def get_audio_handler(self):
        return self._audio_handler

    def save_wave(self):
        self._create_wave()
        wave = self.get_wave()
        wave.setframerate(self._rate)
        wave.setnchannels(self._channels)
        wave.setsampwidth(self.get_audio_handler().get_sample_size(self._format))
        wave.writeframes(b''.join(self.buffers))
        print(f'finshied file name is: {self.get_file()}')

AudioRecorder().run()