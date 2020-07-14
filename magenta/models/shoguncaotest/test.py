import os

from magenta.pipelines import pipeline
from magenta.pipelines import chord_pipelines
from magenta.pipelines import dag_pipeline
import note_seq
import tensorflow.compat.v1 as tf
from magenta.pipelines import event_sequence_pipeline
from magenta.pipelines import note_sequence_pipelines
from magenta.models.shoguncaotest.chord_encoder import ChordEncoder
from note_seq import chords_lib

def get_pipeline():
    dag = {}

    quantizer = note_sequence_pipelines.Quantizer(steps_per_quarter=4)
    dag[quantizer] = dag_pipeline.DagInput(note_seq.NoteSequence)

    achord = chord_pipelines.ChordsExtractor(all_transpositions=False)
    dag[achord] = quantizer

    encoder_pipeline = event_sequence_pipeline.EncoderPipeline(chords_lib.ChordProgression, ChordEncoder(), name='shoguncaoEncoderDecoder')
    dag[encoder_pipeline] = achord

    dag[dag_pipeline.DagOutput('shoguncaoDagOutput')] = encoder_pipeline

    return dag_pipeline.DAGPipeline(dag)

def main(unused_argv):
    input = '/Users/shoguncao/Work/未命名文件夹/output/data.tfrecord'
    output = '/Users/shoguncao/Work/未命名文件夹/output2'
    pipeline_instance = get_pipeline()
    pipeline.run_pipeline_serial(pipeline_instance, pipeline.tf_record_iterator(input, pipeline_instance.input_type), output)

def console_entry_point():
    tf.disable_v2_behavior()
    tf.app.run(main)


if __name__ == '__main__':
  console_entry_point()
